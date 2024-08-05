package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.util.ArrayList;
import java.util.List;
import org.springframework.util.CollectionUtils;

public class SegmentedFeaturedModelHelper {

  private SegmentedFeaturedModelHelper() {}

  public static SegmentedFeaturedModel createSegmentedFeaturedModel(FeaturedModel featuredModel) {
    return new SegmentedFeaturedModel(
        featuredModel.getDirectiveName(),
        featuredModel.getShowTabOn(),
        featuredModel.getTitle(),
        featuredModel.isVisible(),
        featuredModel.getPageId());
  }

  public static void fillNonSegmentedModules(
      FeaturedModel featuredModel, List<AbstractFeaturedModule<?>> nonSegmentedModules) {
    nonSegmentedModules.addAll(
        featuredModel.getModules().stream()
            .parallel()
            .filter(
                (AbstractFeaturedModule<?> module) ->
                    !(module instanceof QuickLinkModule
                            || module instanceof SurfaceBetModule
                            || module instanceof InplayModule
                            || module
                                instanceof
                                EventsModule // EventModule covers HighlightCarouselModule and
                        // SurfaceBetModule as well
                        )
                        || module instanceof PopularBetModule
                        || module instanceof BybWidgetModule)
            .map(
                (AbstractFeaturedModule<?> module) -> {
                  module.setSegmentOrder(module.getDisplayOrder().doubleValue());
                  return module;
                })
            .toList());
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
      List<QuickLinkData> data = getQuickLinkDataFromSegmentView(segmentView);
      quickLinkModule.setData(data);
      quickLinkSurfacebetInplaymodules.add(quickLinkModule);
    }
    if (featuredModel.getSurfaceBetModule() != null) {
      SurfaceBetModule surfaceBetModule =
          featuredModel
              .getSurfaceBetModule()
              .copyWithEmptySegmentedData(
                  featuredModel.getSurfaceBetModule().getDisplayOrder().doubleValue());
      List<SurfaceBetModuleData> data = getSurfaceBetDataFromSegmentView(segmentView);
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
            .map(
                eventModules -> (AbstractFeaturedModule<? extends AbstractModuleData>) eventModules)
            .toList());
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
            .map(
                eventModules -> (AbstractFeaturedModule<? extends AbstractModuleData>) eventModules)
            .toList());
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
        .toList();
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

  public static List<SurfaceBetModuleData> getSurfaceBetDataFromSegmentView(
      SegmentView segmentView) {
    return segmentView.getSurfaceBetModuleData().values().stream()
        .map(
            segMod ->
                (SurfaceBetModuleData)
                    cloneAbstractModuleData(
                        segMod.getSurfaceBetModuleData(), segMod.getSegmentOrder()))
        .toList();
  }

  public static List<QuickLinkData> getQuickLinkDataFromSegmentView(SegmentView segmentView) {
    return segmentView.getQuickLinkData().values().stream()
        .map(
            segMod ->
                (QuickLinkData)
                    cloneAbstractModuleData(segMod.getQuickLinkData(), segMod.getSegmentOrder()))
        .toList();
  }

  public static AbstractModuleData cloneAbstractModuleData(
      AbstractModuleData abstractModuleData, double segmentOrder) {
    AbstractModuleData copy = abstractModuleData.copyWithEmptySegmentedData();
    copy.setSegmentOrder(segmentOrder);
    return copy;
  }
}
