package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static org.springframework.util.CollectionUtils.isEmpty;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector;
import com.coral.oxygen.middleware.pojos.model.cms.Fanzone;
import com.coral.oxygen.middleware.pojos.model.cms.featured.HighlightCarousel;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FanzoneSegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.HighlightCarouselModule;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * This class is used for prepare HighlightCarouselModules for Fanzone Page by interacting with Site
 * Serve and CMS
 */
@Slf4j
@SuppressWarnings("java:S4605")
@Service
@Getter
public class FanzoneHighlightCarouselModuleProcessor extends HighlightCarouselModuleProcessor {
  private final CmsService cmsService;

  private static final String FANZONE21_TEAM_ID = "FZ001";

  public FanzoneHighlightCarouselModuleProcessor(
      SiteServerApi siteServerApi,
      EventDataInjector eventDataInjector,
      MarketsCountInjector marketsCountInjector,
      FeaturedCommentaryInjector commentaryInjector,
      CmsService cmsService) {
    super(siteServerApi, eventDataInjector, marketsCountInjector, commentaryInjector);
    this.cmsService = cmsService;
  }

  /**
   * This method used to construct HighlightCarouselModule from CMS SportModule
   *
   * @param carousel it is CMS HighlightCarousel module
   * @param cmsSportModule it is CMS SportModule
   * @return HighlightCarouselModule
   */
  @Override
  protected HighlightCarouselModule toCarouselModule(
      HighlightCarousel carousel, SportModule cmsSportModule) {
    log.info("Started executing toCarouselModule for fanzone hc ");
    HighlightCarouselModule highlightCarouselModule = new HighlightCarouselModule();
    commontoCarouselModule(highlightCarouselModule, carousel, cmsSportModule);
    validateFanZoneForHC(carousel);
    highlightCarouselModule.setTypeIds(carousel.getTypeIds());
    highlightCarouselModule.setFanzoneSegments(carousel.getFanzoneSegments());
    if (isEmpty(carousel.getTypeIds())) {
      List<Long> eventIdsCMS =
          carousel.getEvents().stream()
              .distinct()
              .map(Long::parseLong)
              .collect(Collectors.toList());
      List<Long> eventIdsSiteServe =
          getEvents(carousel, highlightCarouselModule.getFanzoneSegments());
      eventIdsCMS.retainAll(eventIdsSiteServe);
      highlightCarouselModule.setEventIds(eventIdsCMS);
    } else {
      highlightCarouselModule.setEventIds(
          getEvents(carousel, highlightCarouselModule.getFanzoneSegments()));
    }
    log.info("Ended executing toCarouselModule for fanzone hc ");
    return highlightCarouselModule;
  }

  /**
   * This method used getEvents based on eventids or typeids configured in CMS by making call to
   * Site serve
   *
   * @param carousel CMS HighlightCarousel module is to get typedids or event ids form CMS
   * @param teamIds passing as Value to Simplefilter to site serve call
   * @return EventIDs
   */
  private List<Long> getEvents(HighlightCarousel carousel, List<String> teamIds) {
    log.info("Started executing getEvents for fanzone hc ");
    SimpleFilter eventsFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();
    Predicate<Event> eventPredicate = e -> true;
    if (Boolean.FALSE.equals(carousel.getInPlay())) {
      eventsFilter = excludeLiveEventsFilter();
      eventPredicate = this::isNotLiveEvent;
    }

    Stream<Event> eventStream;
    if (!isEmpty(carousel.getEvents())) {
      eventStream = getEventsByIds(carousel.getEvents(), eventsFilter);
    } else if (!isEmpty(carousel.getTypeIds())) {
      eventStream =
          teamIds.contains(FANZONE21_TEAM_ID)
              ? getEventsByTypes(carousel.getTypeIds(), eventsFilter)
              : getEventsByTypes(
                  carousel.getTypeIds(),
                  fanzoneHCSimpleFilter(teamIds)); // filtering data for 21st team with simplefilter
    } else {
      return new ArrayList<>();
    }
    return fetchEventIds(eventStream, eventPredicate);
  }

  /**
   * Fanzone BMA-62182: Calling SiteServerApi to get Events by passing Fanzone configured TypeIds
   *
   * @param typeIds will be used pass typeids to siteserve Api
   * @param eventsFilter will be used to pass simple filter to SS API to fetch team ids data
   * @return event
   */
  private Stream<Event> getEventsByTypes(List<String> typeIds, SimpleFilter eventsFilter) {
    return getSiteServerApi()
        .getEventForType(typeIds, eventsFilter)
        .map(List::stream)
        .orElse(Stream.empty());
  }

  /**
   * Fanzone BMA-62182 processFanzoneSegmentwiseModules for each Segment
   *
   * @param module is highlightCarousel Module to be processed
   * @param fanzoneSegmentWiseModules it will be used to prepare Fanzone structure for HC
   */
  public void processFanzoneSegmentwiseModules(
      HighlightCarouselModule module, Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules) {
    log.info("Started processFanzoneSegmentwiseModules for hc");
    module
        .getFanzoneSegments()
        .forEach(
            (String teamId) -> {
              FanzoneSegmentView fanzoneSegmentView =
                  fanzoneSegmentWiseModules.containsKey(teamId)
                      ? fanzoneSegmentWiseModules.get(teamId)
                      : new FanzoneSegmentView();

              Map<String, HighlightCarouselModule> highlightCarouselModules =
                  fanzoneSegmentView.getHighlightCarouselModules();
              highlightCarouselModules.put(module.getId(), module);
              fanzoneSegmentWiseModules.put(teamId, fanzoneSegmentView);
              updateFanzoneModuleSegmentView(teamId, module);
            });

    log.info("End processFanzoneSegmentwiseModules for hc");
  }

  /**
   * creating fanzoneModuleSegmentView for each module to get MODULE_CONTENT_CHANGE
   *
   * @param teamId is the unique opta Id of each team
   * @param module is highlightCarousel Module to be processed
   */
  private void updateFanzoneModuleSegmentView(String teamId, HighlightCarouselModule module) {
    Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = module.getFanzoneModuleSegmentView();
    FanzoneSegmentView fanzoneSegmentView =
        fanzoneModuleSegmentView.containsKey(teamId)
            ? fanzoneModuleSegmentView.get(teamId)
            : new FanzoneSegmentView();
    fanzoneSegmentView.getHighlightCarouselModules().put(module.getId(), module);
    fanzoneModuleSegmentView.put(teamId, fanzoneSegmentView);
    module.setFanzoneModuleSegmentView(fanzoneModuleSegmentView);
  }
  /**
   * Fanzone BMA-62182: Validating Fanzone HighlightCarousels and TypeIds with Oxygen-cms-api
   * configured Fanzone PrimaryCompetitionId & SecondaryCompetitionId. Validating Fanzone Segments
   * with Oxygen-cms-api configured Fanzones.
   *
   * @param module it is HC module used for performing Validations
   */
  private void validateFanZoneForHC(HighlightCarousel module) {
    log.info("Started executing validateFanZoneForHC ");
    List<Fanzone> fanZones = new ArrayList<>(cmsService.getFanzones());
    List<String> configFzTypeIds = new ArrayList<>();
    List<String> configFzSegs = new ArrayList<>();
    List<String> hcTypeIds = module.getTypeIds();
    List<String> fanzoneSegments = module.getFanzoneSegments();
    fanZones.forEach(
        (Fanzone fanZone) -> {
          configFzTypeIds.add(fanZone.getPrimaryCompetitionId());
          configFzTypeIds.addAll(Arrays.asList(fanZone.getSecondaryCompetitionId().split(",")));
          configFzSegs.add(fanZone.getTeamId());
        });
    if (!(isEmpty(hcTypeIds))) {
      hcTypeIds.retainAll(configFzTypeIds);
      module.setTypeIds(hcTypeIds);
    }
    if (fanzoneSegments.retainAll(configFzSegs)) {
      module.setFanzoneSegments(fanzoneSegments);
    }
    log.info("Ended executing validateFanZoneForHC ");
  }

  /**
   * this method fanzoneHCSimpleFilter is used to construct SimpleFilter to pass event.TeamExtIds to
   * get specific Fanzone team data from Site serve
   *
   * @param teamids will contain teamids of fanzone segments
   * @return SimpleFilter
   */
  private SimpleFilter fanzoneHCSimpleFilter(List<String> teamids) {
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(
                "event.teamExtIds", BinaryOperation.intersects, toComaSeparatedString(teamids));
    return (SimpleFilter) builder.build();
  }
  /**
   * toComaSeparatedString used to construct List of teamids into "," seperated String
   *
   * @param list it will be teamids data
   * @return String
   */
  private String toComaSeparatedString(List<String> list) {
    return String.join(",", list);
  }
}
