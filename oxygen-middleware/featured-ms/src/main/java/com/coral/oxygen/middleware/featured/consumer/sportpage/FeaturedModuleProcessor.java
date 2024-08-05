package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static com.coral.oxygen.middleware.pojos.model.cms.EventLoadingType.RACING_GRID;
import static com.coral.oxygen.middleware.pojos.model.cms.EventLoadingType.TYPE_ID;

import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.featured.service.BybService;
import com.coral.oxygen.middleware.featured.service.FeaturedDataFilter;
import com.coral.oxygen.middleware.featured.service.injector.*;
import com.coral.oxygen.middleware.pojos.model.cms.Module;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentOrderdModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentView;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@RequiredArgsConstructor
public class FeaturedModuleProcessor implements SegmentOrderProcessor {

  private static final String YC_FLAG = "EVFLAG_YC";
  private static final String FEATURED_MODULE_DIRECTIVE_NAME = "Featured";
  private static final String EVENT_HUB_MODULE_DIRECTIVE_NAME = "EventHub";

  private final EventDataInjector eventDataInjector;
  private final SingleOutcomeEventsModuleInjector singleOutcomeDataInjector;
  private final RacingEventsModuleInjector racingDataInjector;
  private final MarketsCountInjector marketsCountInjector;
  private final FeaturedCommentaryInjector commentaryInjector;
  private final FeaturedDataFilter featuredDataFilter;
  private final SystemConfigProvider systemConfigProvider;
  private final BybService bybService;
  private final DFRacingEventsModuleInjector dfRacingEventsModuleInjector;

  public List<EventsModule> getFirstFeaturedEventModules(
      SportModule cmsModule, ModularContent modularContent, Set<Long> excludedEventIds) {
    return modularContent.stream()
        .filter(
            commonModule ->
                FEATURED_MODULE_DIRECTIVE_NAME.equalsIgnoreCase(commonModule.getDirectiveName())
                    || EVENT_HUB_MODULE_DIRECTIVE_NAME.equalsIgnoreCase(
                        commonModule.getDirectiveName()))
        .findFirst()
        .map(
            featuredItem ->
                processFeaturedData(cmsModule, modularContent, featuredItem, excludedEventIds))
        .orElse(Collections.emptyList());
  }

  private List<EventsModule> processFeaturedData(
      SportModule cmsModule,
      ModularContent modularContent,
      ModularContentItem featuredItem,
      Set<Long> excludedEventIds) {
    try {
      List<Module> filteredFeaturedModules =
          featuredItem.getModules().stream()
              .filter(this::isValidFeaturedModules)
              .collect(Collectors.toList());
      if (cmsModule.getSportId() != 0)
        filteredFeaturedModules =
            removeExcludedEventsModuleData(filteredFeaturedModules, excludedEventIds);

      return handleModulesInParallels(cmsModule, modularContent, filteredFeaturedModules);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Featured Model processing", e);
    }
    return Collections.emptyList();
  }

  private List<Module> removeExcludedEventsModuleData(
      List<Module> filteredFeaturedModules, Set<Long> excludedEventIds) {
    List<Module> result = new ArrayList<>();
    for (Module module : filteredFeaturedModules) {
      if (!CollectionUtils.isEmpty(module.getData())) {

        module.setData(
            module.getData().stream()
                .filter(item -> !excludedEventIds.contains(item.getId()))
                .collect(Collectors.toList()));

        if (!CollectionUtils.isEmpty(module.getData())) {
          module.setTotalEvents(module.getData().size());
          result.add(module);
        }
      }
    }
    return result;
  }

  private boolean isValidFeaturedModules(Module module) {
    return module != null
        && (!module.getData().isEmpty()
            || featuredDataFilter.isRacingGridModule(module.getDataSelection()));
  }

  private List<EventsModule> handleModulesInParallels(
      SportModule cmsModule, ModularContent modularContent, List<Module> modules) {
    return modules.stream()
        .parallel()
        .map(module -> processEventsModule(cmsModule, modularContent, module))
        .collect(Collectors.toList());
  }

  private EventsModule processEventsModule(
      SportModule cmsModule, ModularContent modularContent, Module moduleSection) {
    EventsModule item = new EventsModule(cmsModule, moduleSection);
    try {
      IdsCollector idsCollector = new IdsCollector(modularContent, item);
      List<EventsModuleData> data = item.getData();

      if (!CollectionUtils.isEmpty(data)) {
        eventDataInjector.injectData(data, idsCollector);
        singleOutcomeDataInjector.injectData(data, idsCollector);
        overrideOutcomeDataEventNamesToOutcomeName(data);
        racingDataInjector.injectData(data, idsCollector);
        if (systemConfigProvider.systemConfig().hasRacingDataHub()) {
          dfRacingEventsModuleInjector.injectData(data, idsCollector);
        }
        marketsCountInjector.injectData(data, idsCollector);
        commentaryInjector.injectData(data, idsCollector);
        item.setCategoryId(
            data.stream()
                .map(EventsModuleData::getCategoryId)
                .filter(Objects::nonNull)
                .findAny()
                .orElse(null));
      }

      // MiddleWare never sees events for RacingGrid selection type
      // to keep consistency for all EventModules just map SelectionId to CategoryId
      if (item.getDataSelection().getSelectionType().equals(RACING_GRID.getValue())) {
        item.setCategoryId(item.getDataSelection().getSelectionId());
      }

      return buildOutputModule(item, moduleSection);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      EventsModule eventsModule = new EventsModule();
      eventsModule.setErrorMessage(e.toString());
      log.warn(
          ">>  The featured module # {} was defected by reason [Error Message ]: >> {} ",
          item.getId(),
          e.toString());
      return eventsModule;
    }
  }

  private void overrideOutcomeDataEventNamesToOutcomeName(List<EventsModuleData> items) {
    // relates to BMA-17278 (Make nameOverride more important than outcome name)
    items.stream()
        .filter(
            event ->
                event.getOutcomeId() != null) // only items with outcome Ids should be processed
        .forEach(
            event -> {
              if (!event.getMarkets().isEmpty()) {
                String outcomeName = event.getMarkets().get(0).getOutcomes().get(0).getName();
                if (event.getNameOverride() == null
                    || outcomeName.startsWith(event.getNameOverride())) {
                  event.setName(outcomeName);
                }
              }
            });
  }

  private EventsModule buildOutputModule(EventsModule eventsModule, Module module) {

    if (TYPE_ID.isTypeOf(module.getDataSelection().getSelectionType())) {
      try {
        int typeId = Integer.parseInt(module.getDataSelection().getSelectionId());

        String drilldowns =
            eventsModule.getData().stream()
                .map(EventsModuleData::getDrilldownTagNames)
                .collect(Collectors.joining());

        boolean yourCallAvailableForType =
            bybService.isBuildYourBetAvailableForType(typeId) || drilldowns.contains(YC_FLAG);
        eventsModule.setYourCallAvailable(yourCallAvailableForType);
      } catch (Exception e) {
        log.error("Error parsing typeId for module", e);
      }
    }
    return eventsModule;
  }

  public void processSegmentwiseModules(
      EventsModule module,
      Map<String, SegmentView> segmentWiseModules,
      Map<String, Set<Long>> segmentedExcludedEvents,
      String moduleType) {
    module
        .getSegments()
        .forEach(
            (String seg) -> {
              SegmentView segmentView =
                  segmentWiseModules.containsKey(seg)
                      ? segmentWiseModules.get(seg)
                      : new SegmentView();
              Optional<SegmentReference> segmentReference =
                  module.getSegmentReferences().stream()
                      .filter(
                          segRef ->
                              segRef.getSegment().equals(seg) && segRef.getDisplayOrder() >= 0)
                      .findFirst();

              double sortOrder =
                  segmentReference.isPresent()
                      ? segmentReference.get().getDisplayOrder()
                      : getSortOrderFromSegmentView(segmentView, moduleType);

              double segmentOrder =
                  (module.getDisplayOrder().doubleValue() * MODULE_DISPLAY_ORDER + sortOrder)
                      / MODULE_DISPLAY_ORDER;

              SegmentOrderdModule segmentOrderdModule =
                  new SegmentOrderdModule(segmentOrder, module);
              Set<Long> excludedEvents = segmentedExcludedEvents.get(seg);
              List<EventsModuleData> moduleData = limitEvents(module, excludedEvents);
              segmentOrderdModule.setCashoutAvail(
                  featuredDataFilter.isCashOutAvailable(moduleData));
              segmentOrderdModule.setEventsModuleData(moduleData);
              Set<Long> excludedEventsInThisModule =
                  moduleData.stream().map(EventsModuleData::getId).collect(Collectors.toSet());
              if (!CollectionUtils.isEmpty(excludedEvents)
                  && !CollectionUtils.isEmpty(excludedEventsInThisModule))
                excludedEvents.addAll(excludedEventsInThisModule);
              else if (!CollectionUtils.isEmpty(excludedEventsInThisModule)) {
                excludedEvents = new HashSet<>();
                excludedEvents.addAll(excludedEventsInThisModule);
                segmentedExcludedEvents.put(seg, excludedEvents);
              }

              Map<String, SegmentOrderdModule> eventModules = segmentView.getEventModules();
              eventModules.put(module.getId(), segmentOrderdModule);
              segmentWiseModules.put(seg, segmentView);
              updateModuleSegmentView(seg, module, segmentOrderdModule);
            });
  }

  private void updateModuleSegmentView(
      String segment, EventsModule module, SegmentOrderdModule segmentOrderdModule) {
    Map<String, SegmentView> moduleSegmentView = module.getModuleSegmentView();
    SegmentView segmentView =
        moduleSegmentView.containsKey(segment) ? moduleSegmentView.get(segment) : new SegmentView();
    segmentView.getEventModules().put(module.getId(), segmentOrderdModule);
    moduleSegmentView.put(segment, segmentView);
    module.setModuleSegmentView(moduleSegmentView);
  }

  public List<EventsModuleData> limitEvents(EventsModule module, Set<Long> excludedEvents) {

    List<EventsModuleData> eventsModuleData =
        module.getData().stream()
            .filter(data -> !(excludedEvents != null && excludedEvents.contains(data.getId())))
            .collect(Collectors.toList());
    if (module.getMaxRows() != null && module.getMaxRows() > 0) {
      eventsModuleData = truncated(eventsModuleData, module.getMaxRows());
    }
    return eventsModuleData;
  }

  private <T> List<T> truncated(List<T> list, int maxSize) {
    return list.subList(0, Math.min(list.size(), maxSize));
  }
}
