package com.coral.oxygen.middleware.featured.service.injector;

import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.JsonFacade;
import com.coral.oxygen.middleware.common.service.AbstractCommentaryInjector;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.stereotype.Component;

@Component
public class FeaturedCommentaryInjector extends AbstractCommentaryInjector
    implements EventsModuleInjector {

  public FeaturedCommentaryInjector(
      FeaturedSiteServerService featuredSiteServerService,
      SystemConfigProvider systemConfigProvider) {
    super(featuredSiteServerService, systemConfigProvider);
  }

  @Override
  public void injectData(List<? extends EventsModuleData> items, IdsCollector idsCollector) {
    List<Long> eventsToUpdateIds =
        items.stream()
            .filter(event -> event.getMarkets() != null && !event.getMarkets().isEmpty())
            .filter(event -> Boolean.TRUE.equals(event.getMarkets().get(0).getMarketBetInRun()))
            .map(EventsModuleData::getId)
            .collect(Collectors.toList());

    List<EventsModuleData> events =
        items.stream().filter(event -> event.getId() != null).collect(Collectors.toList());

    injectData(eventsToUpdateIds, events);
  }

  @Override
  protected void populateEvent(EventsModuleData event, Event comments) {
    super.populateEvent(event, comments);
    String categoryCode = event.getCategoryCode();
    if (categoryCode == null) {
      categoryCode = "";
    }
    if ("football".equalsIgnoreCase(categoryCode)) {
      populateLatestPeriod(event, comments);
      populateClockData(event, comments);
    }
  }

  private void populateLatestPeriod(EventsModuleData event, Event comments) {
    Map<String, Object> latestPeriod = extractLatestPeriod(comments);
    if (latestPeriod == null) {
      return;
    }

    Gson gson = JsonFacade.GSON;
    // mandatory deep clone
    latestPeriod = gson.fromJson(gson.toJson(latestPeriod), Map.class);
    if (latestPeriod.get(CommentaryField.CHILDREN) instanceof Collection) {
      Stream<Map> steamOfMaps =
          ((Collection) latestPeriod.get(CommentaryField.CHILDREN))
              .stream().filter(e -> e instanceof Map).map(Map.class::cast);
      List<Map> filteredChildren =
          steamOfMaps
              .filter(map -> map.get("eventPeriodClockState") != null)
              .collect(Collectors.toList());
      latestPeriod.put(CommentaryField.CHILDREN, filteredChildren);
    }
    event.getComments().setLatestPeriod(latestPeriod);
  }
}
