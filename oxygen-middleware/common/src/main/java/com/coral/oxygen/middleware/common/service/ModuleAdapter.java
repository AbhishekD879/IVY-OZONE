package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.JsonFacade;
import com.coral.oxygen.middleware.RuntimeTypeAdapterFactory;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingPosition;
import com.google.gson.Gson;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.CollectionUtils;

/**
 * Anti-entropy adapter.
 *
 * <p>Single point for handling mutation and serialization / deserialization of the featured
 * collections. Abstract approach for prevents growing numbers of utility classes for splitting
 * modules collections by type. Here will be added other methods for casting and processing
 * following modules like quick links, hight-light carousel and etc.
 */
@Slf4j
public abstract class ModuleAdapter {

  public static final Gson FEATURED_GSON;

  static {
    RuntimeTypeAdapterFactory<AbstractFeaturedModule> moduleAdapterFactory =
        RuntimeTypeAdapterFactory.of(AbstractFeaturedModule.class)
            .registerSubtype(QuickLinkModule.class)
            .registerSubtype(EventsModule.class)
            .registerSubtype(RecentlyPlayedGameModule.class)
            .registerSubtype(InplayModule.class)
            .registerSubtype(HighlightCarouselModule.class)
            .registerSubtype(SurfaceBetModule.class)
            .registerSubtype(AemBannersModule.class)
            .registerSubtype(RacingModule.class)
            .registerSubtype(RacingEventsModule.class)
            .registerSubtype(VirtualRaceModule.class)
            .registerSubtype(VirtualEventModule.class)
            .registerSubtype(PopularBetModule.class)
            .registerSubtype(InternationalToteRaceModule.class)
            .registerSubtype(BybWidgetModule.class)
            .registerSubtype(SuperButtonModule.class)
            .registerSubtype(PopularAccaModule.class);

    RuntimeTypeAdapterFactory<AbstractModuleData> dataAdapterFactory =
        RuntimeTypeAdapterFactory.of(AbstractModuleData.class).registerSubtype(QuickLinkData.class);

    FEATURED_GSON =
        JsonFacade.createParser(
            builder ->
                builder
                    .registerTypeAdapterFactory(moduleAdapterFactory)
                    .registerTypeAdapterFactory(dataAdapterFactory));
  }

  // FIXME: strange usage. OOP killer.
  @Deprecated
  protected List<EventsModuleData> toLiveserveEventsData(
      List<AbstractFeaturedModule<?>> featuredModules) {
    List<EventsModuleData> result = new ArrayList<>();
    for (AbstractFeaturedModule<?> module : featuredModules) {
      if (module instanceof EventsModule) {
        result.addAll(((EventsModule) module).getData());
      } else if (module instanceof InplayModule) {
        result.addAll(generateEventsFromInplayModule((InplayModule) module));
      } else if (module instanceof SurfaceBetModule) {
        result.addAll(((SurfaceBetModule) module).getData());
      } else if (module instanceof BybWidgetModule bybWidgetModule) {
        result.addAll(bybWidgetModule.getData());
      } else if (module instanceof PopularAccaModule popularAccaModule) {
        List<PopularBetModuleData> events =
            popularAccaModule.getData().stream()
                .flatMap(data -> data.getPositions().stream())
                .map(TrendingPosition::getEvent)
                .toList();
        result.addAll(events);
      }
    }
    return result;
  }

  // FIXME: used only for tests. remove it.
  @Deprecated
  protected List<EventsModuleData> toEventsModuleData(FeaturedModel featuredModel) {
    return featuredModel.getModules().stream()
        .map(AbstractFeaturedModule::getData)
        .filter(Objects::nonNull)
        .flatMap(Collection::stream)
        .filter(f -> f instanceof EventsModuleData)
        .map(EventsModuleData.class::cast)
        .collect(Collectors.toList());
  }

  private List<EventsModuleData> generateEventsFromInplayModule(InplayModule inplayModule) {
    if (!CollectionUtils.isEmpty(inplayModule.getData())) {
      if (inplayModule.isSegmented()) {
        Set<EventsModuleData> events =
            inplayModule.getModuleSegmentView().values().stream()
                .map(segView -> segView.getInplayModuleData().values())
                .flatMap(Collection::stream)
                .map(SegmentOrderdModuleData::getLimitedEvents)
                .flatMap(Collection::stream)
                .map(SegmentedEvents::getEvents)
                .flatMap(Collection::stream)
                .collect(Collectors.toSet());
        return new ArrayList<>(events);
      } else {
        return inplayModule.getData().stream()
            .map(SportSegment::getEventsByTypeName)
            .flatMap(Collection::stream)
            .map(TypeSegment::getEvents)
            .flatMap(Collection::stream)
            .collect(Collectors.toList());
      }
    } else {
      log.debug(
          "Empty data collection for Inplay module [id: {}, sportId: {}]",
          inplayModule.getId(),
          inplayModule.getSportId());
    }
    return Collections.emptyList();
  }
}
