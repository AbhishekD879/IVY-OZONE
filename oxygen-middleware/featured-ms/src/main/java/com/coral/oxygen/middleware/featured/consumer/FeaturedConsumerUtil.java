package com.coral.oxygen.middleware.featured.consumer;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.HighlightCarouselModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.InplayModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.apache.commons.collections4.CollectionUtils;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class FeaturedConsumerUtil {

  public static void setEventsModuleData(
      Map<Long, EventsModuleData> eventsModuleData,
      AbstractFeaturedModule<?> module,
      List<String> twoUpMarkets) {
    if (module.getModuleType().equals(ModuleType.INPLAY)) {
      ((InplayModule) module)
          .getData()
          .forEach(
              (SportSegment sportSeg) ->
                  sportSeg
                      .getEventsByTypeName()
                      .forEach(
                          (TypeSegment typeSeg) ->
                              typeSeg.setEvents(
                                  typeSeg.getEvents().stream()
                                      .map(
                                          (EventsModuleData eventsData) -> {
                                            if (eventsModuleData.containsKey(eventsData.getId())) {
                                              eventsData = eventsModuleData.get(eventsData.getId());
                                            } else {
                                              eventsModuleData.put(eventsData.getId(), eventsData);
                                            }
                                            return eventsData;
                                          })
                                      .collect(Collectors.toCollection(ArrayList::new)))));
    } else if (module.getData() != null) {
      ((EventsModule) module)
          .setData(
              ((EventsModule) module)
                  .getData().stream()
                      .map(
                          (EventsModuleData eventsData) -> {
                            if (module instanceof HighlightCarouselModule
                                && CollectionUtils.isNotEmpty(twoUpMarkets)
                                && isTwoUpMarketAvailable(eventsData, twoUpMarkets)) {
                              return eventsData;
                            } else if (eventsModuleData.containsKey(eventsData.getId())) {
                              eventsModuleData.get(eventsData.getId()).addModuleId(module.getId());
                              eventsData = eventsModuleData.get(eventsData.getId());
                            } else {
                              eventsData.addModuleId(module.getId());
                              eventsModuleData.put(eventsData.getId(), eventsData);
                            }
                            return eventsData;
                          })
                      .collect(Collectors.toCollection(ArrayList::new)));
    }
  }

  private static boolean isTwoUpMarketAvailable(
      EventsModuleData eventsData, List<String> twoUpmarkets) {
    Predicate<OutputMarket> is2upMarketPresent =
        marketChildren -> twoUpmarkets.contains(marketChildren.getName());
    return eventsData.getMarkets().stream().anyMatch(is2upMarketPresent);
  }

  public static void removeUnusedSportsSegments(InplayModule module) {
    if (!Objects.isNull(module.getData()))
      module.setData(
          module.getData().stream()
              .filter(SportSegment::isUsed)
              .collect(Collectors.toCollection(ArrayList::new)));
  }
}
