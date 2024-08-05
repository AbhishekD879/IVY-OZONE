package com.gvc.oxygen.betreceipts.service.siteserve;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.ExistsFilter.ExistsFilterBuilder;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter.SimpleFilterBuilder;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class SiteServeServiceImpl implements SiteServeService {

  private static final String EVENT_SITE_CHANNELS = "event.siteChannels";
  private static final String EVENT_START_TIME = "event.startTime";
  private static final String CLASS_CATEGORY_ID = "class.categoryId";
  private static final String CLASS_SITE_CHANNELS = "class.siteChannels";
  private static final String CLASS_IS_ACTIVE = "class.isActive";

  private final SiteServerApi siteServerApi;

  @Autowired
  public SiteServeServiceImpl(SiteServerApi siteServerApi) {
    this.siteServerApi = siteServerApi;
  }

  public List<Event> doGetNextRacesEvents(NextEventsParameters params, List<String> classes) {

    SimpleFilter eventsSimpleFilter = buildNextRacesSimpleFilter(params);
    ExistsFilter existsFilter = buildNextRacesExistFilter();

    return siteServerApi
        .getEventToOutcomeForClass(classes, eventsSimpleFilter, limitToFilter(), existsFilter)
        .orElseGet(Collections::emptyList);
  }

  private ExistsFilter buildNextRacesExistFilter() {
    ExistsFilterBuilder existsFilterBuilder = new ExistsFilterBuilder();
    existsFilterBuilder.addBinaryOperation(
        "event:simpleFilter:market.marketStatusCode", BinaryOperation.equals, "A");
    existsFilterBuilder.addBinaryOperation(
        "event:simpleFilter:market.name", BinaryOperation.equals, Market.WIN_OR_EACH_WAY);
    return existsFilterBuilder.build();
  }

  private SimpleFilter buildNextRacesSimpleFilter(NextEventsParameters params) {
    Instant now = Instant.now();
    Instant futureDateTime = now.plus(params.getTimePeriodMinutes(), ChronoUnit.MINUTES);
    return (SimpleFilter)
        new SimpleFilterBuilder()
            .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
            .addBinaryOperation(
                "event.typeFlagCodes",
                BinaryOperation.intersects,
                params.getTypeFlagCodes().toString())
            .addBinaryOperation("market.name", BinaryOperation.equals, Market.WIN_OR_EACH_WAY)
            .addBinaryOperation("market.marketStatusCode", BinaryOperation.equals, "A")
            .addBinaryOperation("event.eventStatusCode", BinaryOperation.equals, "A")
            .addBinaryOperation("event.rawIsOffCode", BinaryOperation.notEquals, "Y")
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThanOrEqual, now)
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.lessThan, futureDateTime)
            .build();
  }

  public List<String> getActiveClassesForCategoryId(int categoryId) {
    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation(CLASS_CATEGORY_ID, BinaryOperation.equals, categoryId)
                .addBinaryOperation(CLASS_SITE_CHANNELS, BinaryOperation.contains, "M")
                .addField(CLASS_IS_ACTIVE)
                .build();
    List<Category> categories =
        siteServerApi.getClasses(simpleFilter, existsFilter()).orElseGet(Collections::emptyList);
    return categories.stream()
        .map(Category::getId)
        .map(String::valueOf)
        .collect(Collectors.toList());
  }

  private LimitToFilter limitToFilter() {
    return new LimitToFilter.LimitToFilterBuilder().build();
  }

  private ExistsFilter existsFilter() {
    return new ExistsFilterBuilder().build();
  }

  private static class Market {

    public static final String WIN_OR_EACH_WAY = "|Win or Each Way|";
  }
}
