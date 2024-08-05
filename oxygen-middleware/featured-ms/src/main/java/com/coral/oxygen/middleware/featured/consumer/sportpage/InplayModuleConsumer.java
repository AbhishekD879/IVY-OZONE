package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.featured.service.InplayDataService;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.InPlayConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.InplayDataSportItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.InplayModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentOrderdModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentedEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@AllArgsConstructor
public class InplayModuleConsumer implements ModuleConsumer<InplayModule>, SegmentOrderProcessor {

  public static final Integer HOME_PAGE_SPORT_ID = 0;
  public static final Integer FOOTBALL = 16;

  private final InplayDataService inplayDataService;

  private final EventDataInjector eventDataInjector;
  private final FeaturedCommentaryInjector featuredCommentaryInjector;

  @Override
  public InplayModule processModule(
      SportPageModule cmsInplayModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds)
      throws SportsModuleProcessException {
    Integer sportId = cmsInplayModule.getSportModule().getSportId();
    try {
      InPlayConfig inplayConfig = getModuleConfigurtion(cmsInplayModule);
      if (!isEventsCountMoreThenZero(inplayConfig)) {
        log.debug(
            "Max inplay events count for sport {} is {}", sportId, inplayConfig.getMaxEventCount());
        InplayModule inplayModule = new InplayModule();
        inplayModule.setErrorMessage("Max count is zero");
        return inplayModule;
      }

      InplayModule module;
      if (sportId.equals(HOME_PAGE_SPORT_ID)) {
        module = buildHomePageModule(inplayConfig);
      } else {
        module = buildSportPageModule(inplayConfig, excludedEventIds);
      }
      module.setId(cmsInplayModule.getSportModule().getId());
      module.setSportId(inplayConfig.getSportId());
      module.setDisplayOrder(cmsInplayModule.getSportModule().getSortOrderOrDefault(null));
      return module;
    } catch (Exception e) {
      return buildModuleWithError(sportId, e);
    }
  }

  @Override
  public List<InplayModule> processModules(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    return null;
  }

  private boolean isEventsCountMoreThenZero(InPlayConfig inplayConfig) {
    boolean maxEventCountPositive = inplayConfig.getMaxEventCount() > 0;
    if (HOME_PAGE_SPORT_ID.equals(inplayConfig.getSportId())) {
      return totalEventsCountForSports(inplayConfig) > 0 && maxEventCountPositive;
    } else {
      return maxEventCountPositive;
    }
  }

  private int totalEventsCountForSports(InPlayConfig inplayConfig) {
    return inplayConfig.getHomeInplaySports().stream()
        .mapToInt(InplayDataSportItem::getEventCount)
        .sum();
  }

  private InPlayConfig getModuleConfigurtion(SportPageModule moduleConfig) {
    return Optional.ofNullable(moduleConfig.getPageData())
        .filter(list -> !list.isEmpty())
        .map(list -> list.get(0)) // only one cms configuration for inplay module for each sportId
        .map(cmsConfig -> (InPlayConfig) cmsConfig)
        .orElseThrow(
            () -> new UnsupportedOperationException("Inplay Module is enabled but not configured"));
  }

  private InplayModule buildModuleWithError(Integer sportId, Exception e) {
    InplayModule module = new InplayModule();
    module.setErrorMessage(e.getMessage());
    NewRelic.noticeError(e);
    log.warn(
        "Inplay module for sportId #{} was defected by reason [Error Message ]: >> {} ",
        sportId,
        e.toString());
    return module;
  }

  private InplayModule buildSportPageModule(InPlayConfig dataItem, Set<Long> excludeEvents) {
    InplayModule module = new InplayModule();
    String version = inplayDataService.getInplayDataVersion();
    SportSegment inplaySportSegment =
        inplayDataService.getSportSegment(version, dataItem.getSportId());
    module.setTotalEvents(countEvents(inplaySportSegment));

    removeExcludedEvents(inplaySportSegment, excludeEvents);

    SportSegment sportSegment = buildSportSegment(inplaySportSegment, dataItem.getMaxEventCount());
    if (StringUtils.isNotEmpty(sportSegment.getCategoryCode())) {
      module.setData(Collections.singletonList(sportSegment));
    }
    return module;
  }

  private InplayModule buildHomePageModule(InPlayConfig inplayConfig) {
    String version = inplayDataService.getInplayDataVersion();

    InPlayData inplayData = inplayDataService.getInplayData(version);
    List<SportSegment> sportSegments = buildHomeSportSegments(inplayData, inplayConfig);

    InplayModule module = new InplayModule();
    module.setTotalEvents(inplayData.getLivenow().getEventCount());
    module.setMaxEventCount(inplayConfig.getMaxEventCount());
    module.setData(sportSegments);
    return module;
  }

  /**
   * 1. remove excluded EventsModuleData 2. remove excluded eventIds from typeSegment.eventIds list
   * 3. decrease typeSegment.eventCount
   */
  private void removeExcludedEvents(SportSegment segment, Set<Long> eventIds) {
    if (CollectionUtils.containsAny(segment.getEventsIds(), eventIds)) {
      segment.getEventsIds().removeAll(eventIds);

      segment
          .getEventsByTypeName()
          .forEach(
              typeSegment -> {
                List<EventsModuleData> excludedEventModuleData =
                    typeSegment.getEvents().stream()
                        .filter(e -> eventIds.contains(e.getId()))
                        .collect(Collectors.toList());

                typeSegment
                    .getEventsIds()
                    .removeAll(
                        excludedEventModuleData.stream()
                            .map(EventsModuleData::getId)
                            .collect(Collectors.toList()));
                typeSegment.getEvents().removeAll(excludedEventModuleData);
                typeSegment.setEventCount(typeSegment.getEvents().size());
                if (CollectionUtils.isEmpty(typeSegment.getEvents())) {
                  log.info(
                      "Removed all events for typeId: {}, consider removing this typeSegment",
                      typeSegment.getTypeId());
                }
              });
    }
  }

  private List<SportSegment> buildHomeSportSegments(
      InPlayData inplayData, InPlayConfig inplayConfig) {
    List<SportSegment> sports = new ArrayList<>();
    for (InplayDataSportItem cmsSportItem : inplayConfig.getHomeInplaySports()) {
      if (doesCategoryHasLiveNow(inplayData, cmsSportItem.getCategoryId())) {
        SportSegment sportSegment =
            inplayDataService.getSportSegment(
                String.valueOf(inplayData.generation()), cmsSportItem.getCategoryId());

        sportSegment.setSegments(cmsSportItem.getSegments());
        sportSegment.setSegmentReferences(cmsSportItem.getSegmentReferences());
        sportSegment.setEventCount(cmsSportItem.getEventCount());

        sortTypesByDisplayOrder(sportSegment);
        injectEventsData(sportSegment);
        if (StringUtils.isNotEmpty(sportSegment.getCategoryCode())) {
          sports.add(sportSegment);
        }
      }
    }
    return sports;
  }

  private SportSegment buildSportSegment(SportSegment sportSegment, int maxEventCount) {
    sortTypesByDisplayOrder(sportSegment);
    sortEventsByStartTime(sportSegment);
    injectEventsData(sportSegment);
    limitEvents(sportSegment, maxEventCount);
    return sportSegment;
  }

  private void injectEventsData(SportSegment sportSegment) {
    sportSegment.getEventsByTypeName().stream()
        .map(TypeSegment::getEvents)
        .forEach(
            events -> {
              IdsCollector idsCollector = new IdsCollector(new ModularContent(), events);
              if (FOOTBALL.equals(sportSegment.getCategoryId())) {
                // in scope of this inject, comments.latestPeriod is been updated, currently, needed
                // only for Football
                eventDataInjector.injectData(events, idsCollector);
              }
              featuredCommentaryInjector.injectData(events, idsCollector);
            });
  }

  private void limitEvents(SportSegment sportSegment, int eventCount) {
    sportSegment.setEventCount(0);
    sportSegment.setEventsIds(new ArrayList<>());
    Iterator<TypeSegment> iterator = sportSegment.getEventsByTypeName().iterator();
    while (iterator.hasNext()) {
      TypeSegment typeSegment = iterator.next();
      if (eventCount == 0) {
        iterator.remove();
        continue;
      }
      List<EventsModuleData> limited =
          typeSegment.getEvents().stream().limit(eventCount).collect(Collectors.toList());
      List<Long> eventIds =
          limited.stream().map(EventsModuleData::getId).collect(Collectors.toList());
      int eventsCount = limited.size();

      typeSegment.setEventsIds(eventIds);
      typeSegment.setEvents(limited);
      typeSegment.setEventCount(eventsCount);

      sportSegment.setEventCount(sportSegment.getEventCount() + eventsCount);
      sportSegment.getEventsIds().addAll(eventIds);

      eventCount -= limited.size();
    }
  }

  private void sortTypesByDisplayOrder(SportSegment sportSegment) {
    sportSegment
        .getEventsByTypeName()
        .sort(
            Comparator.comparing(
                    TypeSegment::getClassDisplayOrder,
                    Comparator.nullsLast(Comparator.naturalOrder()))
                .thenComparing(
                    TypeSegment::getTypeDisplayOrder,
                    Comparator.nullsLast(Comparator.naturalOrder())));
  }

  private void sortEventsByStartTime(SportSegment sportSegment) {
    sportSegment
        .getEventsByTypeName()
        .forEach(
            type -> type.getEvents().sort(Comparator.comparing(EventsModuleData::getStartTime)));
  }

  private Integer countEvents(SportSegment sportSegment) {
    return sportSegment.getEventsByTypeName().stream()
        .map(TypeSegment::getEventCount)
        .mapToInt(Integer::intValue)
        .sum();
  }

  private boolean doesCategoryHasLiveNow(InPlayData inplayData, Integer categoryId) {
    try {
      return inplayData.getLivenow().getSportEvents().stream()
          .anyMatch(sportSegment -> sportSegment.getCategoryId().equals(categoryId));
    } catch (Exception e) {
      return false;
    }
  }

  public void processSegmentwiseModules(
      InplayModule module, Map<String, SegmentView> segmentWiseModules, String moduleType) {
    module
        .getData()
        .forEach(
            (SportSegment data) ->
                data.getSegments()
                    .forEach(
                        (String seg) -> {
                          SegmentView segmentView =
                              segmentWiseModules.containsKey(seg)
                                  ? segmentWiseModules.get(seg)
                                  : new SegmentView();
                          Optional<SegmentReference> segmentReference =
                              data.getSegmentReferences().stream()
                                  .filter(
                                      segRef ->
                                          segRef.getSegment().equalsIgnoreCase(seg)
                                              && segRef.getDisplayOrder() >= 0)
                                  .findFirst();

                          double sortOrder =
                              segmentReference.isPresent()
                                  ? segmentReference.get().getDisplayOrder()
                                  : getSortOrderFromSegmentView(segmentView, moduleType);

                          double segmentOrder =
                              (module.getDisplayOrder().doubleValue() * MODULE_DISPLAY_ORDER
                                      + sortOrder)
                                  / MODULE_DISPLAY_ORDER;
                          SegmentOrderdModuleData segmentOrderdModuleData =
                              new SegmentOrderdModuleData(segmentOrder, data);

                          Map<String, SegmentOrderdModuleData> inPlayModuleData =
                              segmentView.getInplayModuleData();
                          inPlayModuleData.put(data.getCategoryCode(), segmentOrderdModuleData);
                          segmentWiseModules.put(seg, segmentView);
                          updateModuleSegmentView(seg, data, module, segmentOrderdModuleData);
                        }));
  }

  private void updateModuleSegmentView(
      String segment,
      SportSegment data,
      InplayModule module,
      SegmentOrderdModuleData segmentOrderdModuleData) {
    Map<String, SegmentView> moduleSegmentView = module.getModuleSegmentView();
    SegmentView segmentView =
        moduleSegmentView.containsKey(segment) ? moduleSegmentView.get(segment) : new SegmentView();
    segmentView.getInplayModuleData().put(data.getCategoryCode(), segmentOrderdModuleData);
    moduleSegmentView.put(segment, segmentView);
    module.setModuleSegmentView(moduleSegmentView);
  }

  private void limitEvents(
      SportSegment sportSegment,
      SegmentOrderdModuleData segmentOrderdModuleData,
      Set<Long> excludedEvents,
      int eventCount) {
    List<Long> totalEventIds = new ArrayList<>();
    int totalEventsProcessed = 0;
    List<SegmentedEvents> limitedEvents = new ArrayList<>();
    Iterator<TypeSegment> iterator = sportSegment.getEventsByTypeName().iterator();
    while (iterator.hasNext()) {
      TypeSegment typeSegment = iterator.next();
      if (eventCount == 0) {
        break;
      }
      sportSegment.setUsed(true);
      List<EventsModuleData> limited =
          typeSegment.getEvents().stream()
              .filter(
                  eventModuleData ->
                      !(excludedEvents != null && excludedEvents.contains(eventModuleData.getId())))
              .limit(eventCount)
              .collect(Collectors.toList());
      List<Long> eventIds =
          limited.stream().map(EventsModuleData::getId).collect(Collectors.toList());
      int eventsCount = limited.size();

      SegmentedEvents segmentedEvent = new SegmentedEvents();
      segmentedEvent.setEventByTypeName(typeSegment);
      segmentedEvent.setEvents(limited);
      segmentedEvent.setEventIds(eventIds);
      limitedEvents.add(segmentedEvent);

      totalEventsProcessed = totalEventsProcessed + eventsCount;
      totalEventIds.addAll(eventIds);

      eventCount -= limited.size();
    }
    segmentOrderdModuleData.setLimitedEvents(limitedEvents);
    segmentOrderdModuleData.setEventCount(totalEventsProcessed);
    segmentOrderdModuleData.setEventIds(totalEventIds);
  }

  public void limitEvents(
      Map<String, SegmentView> segmentWiseModules,
      InplayModule module,
      Map<String, Set<Long>> segmentedExcludedEvents) {
    segmentWiseModules
        .entrySet()
        .forEach(
            (Map.Entry<String, SegmentView> entry) -> {
              SegmentView segmentView = entry.getValue();
              if (module.getModuleSegmentView().get(entry.getKey()) == null) {
                return;
              }
              Map<String, SegmentOrderdModuleData> inplayModuleData =
                  segmentView.getInplayModuleData();
              int numberOfProcessedEvents = 0;
              LinkedHashMap<String, SegmentOrderdModuleData> inplayModuleDataLinked =
                  new LinkedHashMap<>();

              inplayModuleData.entrySet().stream()
                  .sorted(
                      Collections.reverseOrder(
                          (e1, e2) ->
                              Double.valueOf(e2.getValue().getSegmentOrder())
                                  .compareTo(Double.valueOf(e1.getValue().getSegmentOrder()))))
                  .forEach(sortedEntry -> addToLinkedHashMap(inplayModuleDataLinked, sortedEntry));

              Iterator<String> iterator = inplayModuleDataLinked.keySet().iterator();
              while (iterator.hasNext()) {
                String key = iterator.next();
                SegmentOrderdModuleData segmentOrderdModuleData = inplayModuleDataLinked.get(key);
                SportSegment sportSegment = segmentOrderdModuleData.getInplayData();
                if (numberOfProcessedEvents >= module.getMaxEventCount()) {
                  iterator.remove();
                  continue;
                }
                int sportMaxEvents = sportSegment.getEventCount();
                if (sportMaxEvents + numberOfProcessedEvents > module.getMaxEventCount()) {
                  sportMaxEvents = module.getMaxEventCount() - numberOfProcessedEvents;
                }
                limitEvents(
                    sportSegment,
                    segmentOrderdModuleData,
                    segmentedExcludedEvents.get(entry.getKey()),
                    sportMaxEvents);
                numberOfProcessedEvents += segmentOrderdModuleData.getEventCount();
              }
              segmentView.setInplayModuleData(inplayModuleDataLinked);
              module
                  .getModuleSegmentView()
                  .get(entry.getKey())
                  .setInplayModuleData(inplayModuleDataLinked);
            });
  }

  private void addToLinkedHashMap(
      LinkedHashMap<String, SegmentOrderdModuleData> linkedHashMap,
      Map.Entry<String, SegmentOrderdModuleData> entry) {
    linkedHashMap.put(entry.getKey(), entry.getValue());
  }
}
