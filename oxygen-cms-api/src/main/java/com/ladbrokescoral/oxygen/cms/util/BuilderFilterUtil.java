package com.ladbrokescoral.oxygen.cms.util;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class BuilderFilterUtil {

  private static final String EVENT_CATEGORY_ID = "event.categoryId";
  private static final String EVENT_SITE_CHANNELS = "event.siteChannels";
  private static final String EVENT_SUSPEND_AT_TIME = "event.suspendAtTime";
  private static final String EVENT_IS_STARTED = "event.isStarted";
  private static final String EVENT_DRILLDOWN_TAG_NAMES = "event.drilldownTagNames";
  private static final String EVENT_IS_ACTIVE = "event.isActive";
  private static final String EVENT_START_TIME = "event.startTime";
  private static final String EVENT_IS_LIVE_NOW = "event.isLiveNowEvent";
  private static final String EVENT_SORT_CODE = "event.eventSortCode";
  private static final String EVENT_MARKET_IS_DISPLAYED = "event:simpleFilter:market.isDisplayed";
  private static final String EVENT_MARKET_IS_RESULTED = "event:simpleFilter:market.isResulted";
  private static final String TEMPLATE_MARKET_NAME = "market.templateMarketName";
  private static final String EVENT_IS_DISPLAYED = "event.isDisplayed";

  private static final String EVENT_SORTCODES = "TNMT,MTCH";

  private static final String TEMPLATE_MARKETS = "|2 Ball Betting|,|3 Ball Betting|";

  private static final Instant now = nowUtcWithoutMillis();
  private static final String MARKET_BET_IN_RUN = "event:simpleFilter:market.isMarketBetInRun";

  private static final int DURATION_24_HOURS = 24;
  private static final String BET_INPLAY_DRILLDOWN_TAG = "EVFLAG_BL";

  public static SimpleFilter.SimpleFilterBuilder getLiveEventsFilterBuilder(SportCategory sport) {
    return new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, sport.getCategoryId())
        .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addBinaryOperation(
            EVENT_DRILLDOWN_TAG_NAMES, BinaryOperation.intersects, BET_INPLAY_DRILLDOWN_TAG)
        .addField(EVENT_IS_STARTED)
        .addField(EVENT_IS_LIVE_NOW)
        .addBinaryOperation(
            EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, nowUtcWithoutMillis());
  }

  public static ExistsFilter getEventMarketIsAvailableFilter() {
    return (ExistsFilter)
        new ExistsFilter.ExistsFilterBuilder()
            .addField(MARKET_BET_IN_RUN)
            .addField(EVENT_MARKET_IS_DISPLAYED)
            .addUnaryOperation(EVENT_MARKET_IS_RESULTED, UnaryOperation.isFalse)
            .build();
  }

  public static SimpleFilter.SimpleFilterBuilder getUpcomingEventExistsforMatchesTabBuilder(
      SportCategory sport) {
    return new SimpleFilter.SimpleFilterBuilder()
        .addField(EVENT_IS_ACTIVE)
        .addField(EVENT_IS_DISPLAYED)
        .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, sport.getCategoryId())
        .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addBinaryOperation(EVENT_SORT_CODE, BinaryOperation.equals, "MTCH")
        .addUnaryOperation(EVENT_IS_STARTED, UnaryOperation.isFalse)
        .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThan, now)
        .addBinaryOperation(EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, now)
        .addBinaryOperation(TEMPLATE_MARKET_NAME, BinaryOperation.intersects, TEMPLATE_MARKETS);
  }

  public static ExistsFilter getExistsFilter() {
    return (ExistsFilter)
        new ExistsFilter.ExistsFilterBuilder()
            .addField(EVENT_MARKET_IS_DISPLAYED)
            .addUnaryOperation(EVENT_MARKET_IS_RESULTED, UnaryOperation.isFalse)
            .build();
  }

  public static SimpleFilter.SimpleFilterBuilder getLiveEventExistsforMatchesTabBuilder(
      SportCategory sport) {

    return new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, sport.getCategoryId())
        .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addBinaryOperation(EVENT_SORT_CODE, BinaryOperation.equals, "MTCH")
        .addBinaryOperation(
            EVENT_DRILLDOWN_TAG_NAMES, BinaryOperation.intersects, BET_INPLAY_DRILLDOWN_TAG)
        .addBinaryOperation(TEMPLATE_MARKET_NAME, BinaryOperation.notEquals, "|Outright|")
        .addField(EVENT_IS_STARTED)
        .addField(EVENT_IS_LIVE_NOW)
        .addField(EVENT_IS_DISPLAYED)
        .addField(EVENT_IS_ACTIVE)
        .addBinaryOperation(
            EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, nowUtcWithoutMillis());
  }

  public static SimpleFilter.SimpleFilterBuilder getUpcomingEventExistsForNext24HBuilder(
      SportCategory sport) {
    Instant in24Hours = nowUtcWithoutMillis().plus(Duration.ofHours(DURATION_24_HOURS));
    return new SimpleFilter.SimpleFilterBuilder()
        .addField(EVENT_IS_ACTIVE)
        .addField(EVENT_IS_DISPLAYED)
        .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, sport.getCategoryId())
        .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addUnaryOperation(EVENT_IS_STARTED, UnaryOperation.isFalse)
        .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThan, now)
        .addBinaryOperation(EVENT_START_TIME, BinaryOperation.lessThan, in24Hours)
        .addBinaryOperation(EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, now);
  }

  public static SimpleFilter.SimpleFilterBuilder getUpcomingEventBuilder(SportCategory sport) {
    return new SimpleFilter.SimpleFilterBuilder()
        .addField(EVENT_IS_ACTIVE)
        .addField(EVENT_IS_DISPLAYED)
        .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, sport.getCategoryId())
        .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addUnaryOperation(EVENT_IS_STARTED, UnaryOperation.isFalse)
        .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThan, now)
        .addBinaryOperation(EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, now);
  }

  private static Instant nowUtcWithoutMillis() {
    return Instant.now().truncatedTo(ChronoUnit.SECONDS);
  }
}
