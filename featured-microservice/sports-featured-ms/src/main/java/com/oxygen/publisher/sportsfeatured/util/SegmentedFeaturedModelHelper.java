package com.oxygen.publisher.sportsfeatured.util;

import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.SegmentedFeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.AbstractModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.FanBetsConfig;
import com.oxygen.publisher.sportsfeatured.model.module.data.TeamBetsConfig;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.util.CollectionUtils;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
@Slf4j
public class SegmentedFeaturedModelHelper {

  private static final String FANZONE21ST_TEAMID = "FZ001";

  public static SegmentedFeaturedModel createSegmentedFeaturedModel(FeaturedModel featuredModel) {
    return new SegmentedFeaturedModel(
        featuredModel.getDirectiveName(),
        featuredModel.getShowTabOn(),
        featuredModel.getTitle(),
        featuredModel.isVisible(),
        featuredModel.getPageId(),
        featuredModel.isUseFSCCached());
  }

  public static void fillNonSegmentedModules(
      FeaturedModel featuredModel, List<AbstractFeaturedModule<?>> nonSegmentedModules) {
    nonSegmentedModules.addAll(
        featuredModel.getModules().stream()
            .parallel()
            .filter(
                (AbstractFeaturedModule<?> module) ->
                    !isQuickLinkInplayEventsModule(module)
                        || module instanceof PopularBetModule
                        || module instanceof BybWidgetModule
                        || module instanceof PopularAccaModule)
            .map(
                (AbstractFeaturedModule<?> module) -> {
                  module.setSegmentOrder(module.getDisplayOrder().doubleValue());
                  return module;
                })
            .toList());
  }

  private static boolean isQuickLinkInplayEventsModule(AbstractFeaturedModule<?> module) {
    return module instanceof QuickLinkModule
        || module instanceof InplayModule
        || module instanceof EventsModule;
  }

  public static void populateSegmentedFeaturedModel(
      FeaturedModel featuredModel,
      SegmentedFeaturedModel segmentedFeaturedModel,
      SegmentView segmentView) {
    List<AbstractFeaturedModule<?>> quickLinkSurfacebetInplaymodules = new ArrayList<>();
    addHighlightCarouselModuleFromSegmentView(segmentView, segmentedFeaturedModel);
    addEventModuleFromSegmentView(segmentView, segmentedFeaturedModel);
    if (featuredModel.getQuickLinkModule() != null) {
      QuickLinkModule quickLinkModule =
          featuredModel
              .getQuickLinkModule()
              .copyWithEmptySegmentedData(
                  featuredModel.getQuickLinkModule().getDisplayOrder().doubleValue());
      List<AbstractModuleData> data = getQuickLinkDataFromSegmentView(segmentView);
      quickLinkModule.setData(data);
      quickLinkSurfacebetInplaymodules.add(quickLinkModule);
    }
    if (featuredModel.getSurfaceBetModule() != null) {
      SurfaceBetModule surfaceBetModule =
          (SurfaceBetModule)
              featuredModel
                  .getSurfaceBetModule()
                  .copyWithEmptySegmentedData(
                      featuredModel.getSurfaceBetModule().getDisplayOrder().doubleValue());
      List<EventsModuleData> data = getSurfaceBetDataFromSegmentView(segmentView);
      surfaceBetModule.setData(data);
      quickLinkSurfacebetInplaymodules.add(surfaceBetModule);
    }
    if (featuredModel.getInplayModule() != null) {
      InplayModule inplayModule =
          featuredModel
              .getInplayModule()
              .copyWithEmptySegmentedData(
                  featuredModel.getInplayModule().getDisplayOrder().doubleValue());
      List<SportSegment> data = getInplayModuleDataFromSegmentView(segmentView);
      inplayModule.setData(data);
      quickLinkSurfacebetInplaymodules.add(inplayModule);
    }
    if (!quickLinkSurfacebetInplaymodules.isEmpty())
      segmentedFeaturedModel.addModules(quickLinkSurfacebetInplaymodules);
  }

  private static void addHighlightCarouselModuleFromSegmentView(
      SegmentView segmentView, SegmentedFeaturedModel segmentedFeaturedModel) {
    segmentedFeaturedModel.addModules(
        segmentView.getHighlightCarouselModules().values().stream()
            .map(
                segMod ->
                    segMod.getHighlightCarouselModule().copyWithData(segMod.getSegmentOrder()))
            .collect(Collectors.toList()));
  }

  private static void addEventModuleFromSegmentView(
      SegmentView segmentView, SegmentedFeaturedModel segmentedFeaturedModel) {
    segmentedFeaturedModel.addModules(
        segmentView.getEventModules().values().stream()
            .map(
                (SegmentOrderdModule segMod) -> {
                  EventsModule eventsModule =
                      segMod.getEventsModule().copyWithEmptySegmentedData(segMod.getSegmentOrder());
                  if (Boolean.TRUE.equals(eventsModule.getShowExpanded())) {
                    eventsModule.setData(segMod.getEventsModuleData());
                  }
                  if (!CollectionUtils.isEmpty(segMod.getEventsModuleData()))
                    eventsModule.setTotalEvents(segMod.getEventsModuleData().size());
                  eventsModule.setCashoutAvail(segMod.getCashoutAvail());
                  return eventsModule;
                })
            .collect(Collectors.toList()));
  }

  public static List<SportSegment> getInplayModuleDataFromSegmentView(SegmentView segmentView) {
    return segmentView.getInplayModuleData().values().stream()
        .map(
            (SegmentOrderdModuleData segMod) -> {
              SportSegment sportSegment =
                  (SportSegment)
                      cloneAbstractModuleData(segMod.getInplayData(), segMod.getSegmentOrder());
              setSportSegmentData(sportSegment, segMod);
              return sportSegment;
            })
        .collect(Collectors.toList());
  }

  public static void setSportSegmentData(
      SportSegment sportSegment, SegmentOrderdModuleData segMod) {
    sportSegment.setEventsIds(segMod.getEventIds());
    sportSegment.setEventCount(segMod.getEventCount());
    List<TypeSegment> eventsByTypeName = new ArrayList<>();
    segMod
        .getLimitedEvents()
        .forEach(
            (SegmentedEvents segEvent) -> {
              TypeSegment typeSegment = segEvent.getEventByTypeName().cloneWithEmptyEvents();
              typeSegment.setEvents(segEvent.getEvents());
              typeSegment.setEventsIds(segEvent.getEventIds());
              typeSegment.setEventCount(segEvent.getEvents().size());
              eventsByTypeName.add(typeSegment);
            });
    sportSegment.setEventsByTypeName(eventsByTypeName);
  }

  public static List<EventsModuleData> getSurfaceBetDataFromSegmentView(SegmentView segmentView) {
    return segmentView.getSurfaceBetModuleData().values().stream()
        .map(
            segMod ->
                (EventsModuleData)
                    cloneAbstractModuleData(
                        segMod.getSurfaceBetModuleData(), segMod.getSegmentOrder()))
        .collect(Collectors.toList());
  }

  public static List<AbstractModuleData> getQuickLinkDataFromSegmentView(SegmentView segmentView) {
    return segmentView.getQuickLinkData().values().stream()
        .map(segMod -> cloneAbstractModuleData(segMod.getQuickLinkData(), segMod.getSegmentOrder()))
        .collect(Collectors.toList());
  }

  /**
   * Fanzone BMA-62182: populateFanzoneSegmentedFeaturedModel
   *
   * @param featuredModel
   * @param segmentedFeaturedModel
   * @param fanzoneSegmentView
   * @param segment
   */
  public static void populateFanzoneSegmentedFeaturedModel(
      FeaturedModel featuredModel,
      SegmentedFeaturedModel segmentedFeaturedModel,
      FanzoneSegmentView fanzoneSegmentView,
      String segment) {
    log.info("Started executing populateFanzoneSegmentedFeaturedModel ");
    List<AbstractFeaturedModule<?>> surfacebetmodules = new ArrayList<>();
    List<AbstractFeaturedModule<?>> quickLinkModules = new ArrayList<>();
    if (FANZONE21ST_TEAMID.equals(segment)) {
      segmentedFeaturedModel.addModules(
          new ArrayList<>(fanzoneSegmentView.getHighlightCarouselModules().values()));
    } else {
      segmentedFeaturedModel.addModules(
          filterSegmentedHC(
              fanzoneSegmentView.getHighlightCarouselModules().values().stream()
                  .map(segMod -> segMod.copyWithData(segMod.getSegmentOrder()))
                  .collect(Collectors.toList()),
              segment));
    }
    if (featuredModel.getSurfaceBetModule() != null) {
      SurfaceBetModule surfaceBetModule =
          (SurfaceBetModule)
              featuredModel
                  .getSurfaceBetModule()
                  .copyWithEmptySegmentedData(
                      featuredModel.getSurfaceBetModule().getDisplayOrder().doubleValue());
      List<EventsModuleData> data =
          fanzoneSegmentView.getSurfaceBetModuleData().values().stream()
              .collect(Collectors.toList());
      surfaceBetModule.setData(data);
      surfacebetmodules.add(surfaceBetModule);
    }
    if (!surfacebetmodules.isEmpty()) segmentedFeaturedModel.addModules(surfacebetmodules);

    if (featuredModel.getQuickLinkModule() != null) {
      QuickLinkModule quickLinkModule =
          featuredModel
              .getQuickLinkModule()
              .copyWithEmptySegmentedData(
                  featuredModel.getQuickLinkModule().getDisplayOrder().doubleValue());
      List<AbstractModuleData> data =
          fanzoneSegmentView.getQuickLinkModuleData().values().stream()
              .map(
                  quickLinkData ->
                      cloneAbstractModuleData(quickLinkData, quickLinkData.getSegmentOrder()))
              .filter(quickLinkData -> quickLinkData.getFanzoneSegments().contains(segment))
              .collect(Collectors.toList());
      quickLinkModule.setData(data);
      quickLinkModules.add(quickLinkModule);
    }
    if (!quickLinkModules.isEmpty()) segmentedFeaturedModel.addModules(quickLinkModules);

    List<AbstractFeaturedModule<?>> teamBetModules = new ArrayList<>();
    if (featuredModel.getTeamBetsModule() != null) {
      TeamBetsModule teamBetsModule =
          featuredModel
              .getTeamBetsModule()
              .copyWithEmptySegmentedData(
                  featuredModel.getTeamBetsModule().getDisplayOrder().doubleValue());

      List<TeamBetsConfig> data =
          fanzoneSegmentView.getTeamBetsModuleData().values().stream().toList();
      teamBetsModule.setData(data);
      teamBetModules.add(teamBetsModule);
    }
    if (!teamBetModules.isEmpty()) segmentedFeaturedModel.addModules(teamBetModules);

    List<AbstractFeaturedModule<?>> fanBetModules = new ArrayList<>();
    if (featuredModel.getFanBetsModule() != null) {
      FanBetsModule fanBetsModule =
          featuredModel
              .getFanBetsModule()
              .copyWithEmptySegmentedData(
                  featuredModel.getFanBetsModule().getDisplayOrder().doubleValue());

      List<FanBetsConfig> data =
          fanzoneSegmentView.getFanBetsModuleData().values().stream().toList();
      fanBetsModule.setData(data);
      fanBetModules.add(fanBetsModule);
    }
    if (!fanBetModules.isEmpty()) segmentedFeaturedModel.addModules(fanBetModules);
    log.info("Ended executing populateFanzoneSegmentedFeaturedModel ");
  }

  /**
   * Filtering Segmented data for specific fanzone
   *
   * @param eventModules
   * @param teamId
   * @return segmentedHClist
   */
  private static List<AbstractFeaturedModule<?>> filterSegmentedHC(
      List<EventsModule> eventModules, String teamId) {
    log.info("Started executing filterSegmentedHC");
    List<AbstractFeaturedModule<?>> segmentedHighlightCarousels = new ArrayList<>();
    for (EventsModule eventModule : eventModules) {
      List<Long> eventIds = new ArrayList<>();
      List<EventsModuleData> segmentedEventsModuleData = new ArrayList<>();
      for (EventsModuleData eventModuleData : eventModule.getData()) {
        if (StringUtils.isNotBlank(eventModuleData.getTeamExtIds())
            && eventModuleData.getTeamExtIds().contains(teamId)) {
          segmentedEventsModuleData.add(eventModuleData);
          eventIds.add(Long.parseLong(eventModuleData.getId()));
        }
      }
      eventModule.setData(segmentedEventsModuleData);
      eventModule.setTotalEvents(eventIds.size());
      segmentedHighlightCarousels.add(eventModule);
    }
    log.info("Ended executing filterSegmentedHC ");
    return segmentedHighlightCarousels;
  }

  public static AbstractModuleData cloneAbstractModuleData(
      AbstractModuleData abstractModuleData, double segmentOrder) {
    AbstractModuleData copy = abstractModuleData.copyWithEmptySegmentedData();
    copy.setSegmentOrder(segmentOrder);
    return copy;
  }
}
