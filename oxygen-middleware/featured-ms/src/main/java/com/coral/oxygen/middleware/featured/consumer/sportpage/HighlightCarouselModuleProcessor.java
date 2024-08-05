package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static org.apache.commons.lang3.BooleanUtils.isTrue;
import static org.springframework.util.CollectionUtils.isEmpty;

import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.HighlightCarousel;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.HighlightCarouselModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentOrderdModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentView;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.math.BigDecimal;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@RequiredArgsConstructor
@Data
public class HighlightCarouselModuleProcessor
    implements ModuleConsumer<HighlightCarouselModule>, SegmentOrderProcessor {
  private final SiteServerApi siteServerApi;
  private final EventDataInjector eventDataInjector;
  private final MarketsCountInjector marketsCountInjector;
  private final FeaturedCommentaryInjector commentaryInjector;
  private static final String PRIMARY = "PrimaryMarket";
  private static final String TWO_UP_MARKET = "2UpMarket";

  @Override
  public HighlightCarouselModule processModule(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds)
      throws SportsModuleProcessException {
    throw new UnsupportedOperationException(
        "HighlightCarouselModuleProcessor unsupported this operation.");
  }

  @Override
  public List<HighlightCarouselModule> processModules(
      SportPageModule sportPageModule,
      CmsSystemConfig cmsSystemConfig,
      Set<Long> excludedEventIds) {
    try {
      SportModule cmsSportModule = sportPageModule.getSportModule();
      return sportPageModule.getPageData().stream()
          .filter(HighlightCarousel.class::isInstance)
          .map(HighlightCarousel.class::cast)
          .map(
              carousel -> {
                HighlightCarouselModule module = toCarouselModule(carousel, cmsSportModule);
                module.setData(
                    module.getEventIds().stream()
                        .map(this::initEventData)
                        .collect(Collectors.toCollection(ArrayList::new)));
                eventDataInjector.injectData(
                    module.getData(),
                    new IdsCollector(module.getEventIds()),
                    carousel.getDisplayMarketType());
                marketsCountInjector.injectData(
                    module.getData(), new IdsCollector(module.getEventIds()));
                commentaryInjector.injectData(
                    module.getData(), new IdsCollector(module.getEventIds()));
                return module;
              })
          .map(this::filterEvents)
          .collect(Collectors.toCollection(ArrayList::new));

    } catch (Exception e) {
      log.error("HighlightCarouselModuleProcessor -> ", e);
      return Collections.emptyList();
    }
  }

  private HighlightCarouselModule filterEvents(HighlightCarouselModule carousel) {
    carousel.getData().removeIf(event -> shouldBeExcluded(event, carousel.getInPlay()));
    carousel.setEventIds(
        carousel.getData().stream()
            .map(EventsModuleData::getId)
            .collect(Collectors.toCollection(ArrayList::new)));
    return carousel;
  }

  private boolean shouldBeExcluded(EventsModuleData event, boolean includeInPlay) {
    return isTrue(event.getFinished())
        || (!includeInPlay && isTrue(event.getEventIsLive()))
        || !pricesPresent(event);
  }

  private boolean pricesPresent(EventsModuleData event) {
    return event.getMarkets().stream()
        .flatMap(m -> m.getOutcomes().stream())
        // ignoring SP prices as well
        .anyMatch(o -> !CollectionUtils.isEmpty(o.getPrices()));
  }

  public void applyLimits(List<AbstractFeaturedModule<?>> modules) {
    modules.stream()
        .filter(HighlightCarouselModule.class::isInstance)
        .map(HighlightCarouselModule.class::cast)
        .forEach(this::applyLimits);
  }

  private EventsModuleData initEventData(Long id) {
    EventsModuleData eventsModuleData = new EventsModuleData();

    eventsModuleData.setId(id);

    return eventsModuleData;
  }

  protected HighlightCarouselModule toCarouselModule(
      HighlightCarousel carousel, SportModule cmsSportModule) {
    HighlightCarouselModule highlightCarouselModule = new HighlightCarouselModule();
    commontoCarouselModule(highlightCarouselModule, carousel, cmsSportModule);
    if (carousel.getTypeId() == null) {
      List<Long> eventIdsCMS =
          carousel.getEvents().stream()
              .distinct()
              .map(Long::parseLong)
              .collect(Collectors.toCollection(ArrayList::new));
      List<Long> eventIdsSiteServe = getEvents(carousel);
      eventIdsCMS.retainAll(eventIdsSiteServe);
      highlightCarouselModule.setEventIds(eventIdsCMS);
    } else {
      highlightCarouselModule.setEventIds(getEvents(carousel));
    }
    return highlightCarouselModule;
  }

  /**
   * This method used to reduce duplicate code for Fanzone HighlightCarouselModule and Existing
   * HighlightCarouselModule process
   *
   * @param highlightCarouselModule it is HighlightCarouselModule mapped from CMS module
   * @param carousel it is CMS module
   * @param cmsSportModule it is CMS sportmodule data
   */
  protected void commontoCarouselModule(
      HighlightCarouselModule highlightCarouselModule,
      HighlightCarousel carousel,
      SportModule cmsSportModule) {
    highlightCarouselModule.setId(carousel.getId());
    highlightCarouselModule.setInPlay(
        carousel.getInPlay() == null ? Boolean.TRUE : carousel.getInPlay());
    highlightCarouselModule.setLimit(carousel.getLimit());
    highlightCarouselModule.setSportId(carousel.getSportId());
    highlightCarouselModule.setSvgId(carousel.getSvgId());
    highlightCarouselModule.setTitle(carousel.getTitle());
    highlightCarouselModule.setDisplayOrder(cmsSportModule.getSortOrderOrDefault(null));
    highlightCarouselModule.setSecondaryDisplayOrder(getDisplayOrder(carousel));
    highlightCarouselModule.setPageType(carousel.getPageType());
    highlightCarouselModule.setTypeId(carousel.getTypeId());
    highlightCarouselModule.setSegments(carousel.getSegments());
    highlightCarouselModule.setSegmentReferences(carousel.getSegmentReferences());
    highlightCarouselModule.setDisplayMarketType(
        carousel.getDisplayMarketType() == null ? PRIMARY : carousel.getDisplayMarketType());
    highlightCarouselModule.setDisplayMarketType(carousel.getDisplayMarketType());
    highlightCarouselModule.setDisplayOnDesktop(carousel.getDisplayOnDesktop());
  }

  protected BigDecimal getDisplayOrder(HighlightCarousel carousel) {
    return carousel.getDisplayOrder() == null
        ? BigDecimal.ZERO
        : BigDecimal.valueOf(carousel.getDisplayOrder());
  }

  private List<Long> getEvents(HighlightCarousel carousel) {
    SimpleFilter eventsFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();
    Predicate<Event> eventPredicate = e -> true;
    if (Boolean.FALSE.equals(carousel.getInPlay())) {
      eventsFilter = excludeLiveEventsFilter();
      eventPredicate = this::isNotLiveEvent;
    }

    Stream<Event> eventStream;
    if (!isEmpty(carousel.getEvents())) {
      eventStream = getEventsByIds(carousel.getEvents(), eventsFilter);
    } else if (carousel.getTypeId() != null) {
      eventStream = getEventsByType(carousel.getTypeId(), eventsFilter);
    } else {
      return new ArrayList<>();
    }
    return fetchEventIds(eventStream, eventPredicate);
  }

  protected boolean isNotLiveEvent(Event e) {
    boolean containsBetInPlayFlag =
        e.getDrilldownTagNames() != null
            && Arrays.asList(e.getDrilldownTagNames().split(",")).contains("EVFLAG_BL");
    boolean isInPlayEvent =
        containsBetInPlayFlag
            && Boolean.TRUE.equals(e.getIsLiveNowEvent())
            && Boolean.TRUE.equals(e.getIsStarted());
    return !isInPlayEvent;
  }

  protected Stream<Event> getEventsByIds(List<String> eventIds, SimpleFilter eventsFilter) {
    List<String> prune = new ArrayList<>();
    return siteServerApi
        .getEventToOutcomeForEvent(eventIds, eventsFilter, null, prune)
        .map(List::stream)
        .orElse(Stream.empty())
        .map(Children::getEvent)
        .filter(Objects::nonNull);
  }

  private Stream<Event> getEventsByType(Integer typeId, SimpleFilter eventsFilter) {
    return siteServerApi
        .getEventForType(String.valueOf(typeId), eventsFilter)
        .map(List::stream)
        .orElse(Stream.empty());
  }

  protected List<Long> fetchEventIds(Stream<Event> eventStream, Predicate<Event> eventPredicate) {
    return eventStream
        .filter(eventPredicate)
        .map(Event::getId)
        .map(Long::parseLong)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  protected SimpleFilter excludeLiveEventsFilter() {
    return (SimpleFilter)
        new SimpleFilter.SimpleFilterBuilder()
            .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
            .addUnaryOperation("event.isLiveNowEvent", UnaryOperation.isFalse)
            .build();
  }

  private void applyLimits(HighlightCarouselModule carouselModule) {
    List<EventsModuleData> limitedData = carouselModule.getData();
    if (carouselModule.getLimit() != null) {
      limitedData =
          carouselModule.getData().stream()
              .limit(carouselModule.getLimit())
              .collect(Collectors.toCollection(ArrayList::new));
    }
    carouselModule.setData(limitedData);
    carouselModule.setTotalEvents(limitedData.size());
    carouselModule.setEventIds(
        limitedData.stream()
            .map(EventsModuleData::getId)
            .collect(Collectors.toCollection(ArrayList::new)));

    if (TWO_UP_MARKET.equals(carouselModule.getDisplayMarketType())) {
      carouselModule.setMarketIds(
          carouselModule.getData().stream()
              .map(EventsModuleData::getMarkets)
              .flatMap(List::stream)
              .map(OutputMarket::getId)
              .collect(Collectors.toCollection(ArrayList::new)));
    }
  }

  public void processSegmentwiseModules(
      HighlightCarouselModule module,
      Map<String, SegmentView> segmentWiseModules,
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

              Map<String, SegmentOrderdModule> highlightCarouselModules =
                  segmentView.getHighlightCarouselModules();
              highlightCarouselModules.put(module.getId(), segmentOrderdModule);
              segmentWiseModules.put(seg, segmentView);
              updateModuleSegmentView(seg, module, segmentOrderdModule);
            });
  }

  private void updateModuleSegmentView(
      String segment, HighlightCarouselModule module, SegmentOrderdModule segmentOrderdModule) {
    Map<String, SegmentView> moduleSegmentView = module.getModuleSegmentView();
    SegmentView segmentView =
        moduleSegmentView.containsKey(segment) ? moduleSegmentView.get(segment) : new SegmentView();
    segmentView.getHighlightCarouselModules().put(module.getId(), segmentOrderdModule);
    moduleSegmentView.put(segment, segmentView);
    module.setModuleSegmentView(moduleSegmentView);
  }
}
