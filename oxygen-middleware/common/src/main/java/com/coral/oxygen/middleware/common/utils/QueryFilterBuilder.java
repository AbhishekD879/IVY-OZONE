package com.coral.oxygen.middleware.common.utils;

import static com.coral.oxygen.middleware.common.service.DateTimeHelper.trimToTenSeconds;
import static com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets.*;

import com.coral.oxygen.middleware.common.service.DateTimeHelper;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import com.egalacoral.spark.siteserver.api.*;
import java.time.*;
import java.util.Collection;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@SuppressWarnings("java:S1448")
public class QueryFilterBuilder {

  private static final String EVFLAG_BL = "EVFLAG_BL";
  private static final String EVFLAG_IHR = "EVFLAG_IHR";
  public static final ZoneId GMT_ZONE_ID = ZoneId.of("GMT");
  public static final String MARKET_DISP_SORT_NAME = "market.dispSortName";
  public static final String MR_HH_3_W_2_W = "MR,HH,3W,2W";

  private final MarketTemplateNameService marketTemplateNameService;
  private static final String EVENT_DRILLDOWN_TAGNAMES = "event.drilldownTagNames";
  private static final String ENHANCED_MULTIPLES = "|Enhanced Multiples|";
  private static final int LIVE_EVENT_MAX_DAYS = 5;
  private static final int UPCOMING_EVENT_MAX_HOURS = 24;

  private static final int OUTCOME_LIMIT = 3;

  @Value("${ihr.max.minutes}")
  private String iHRMaxMinutes;

  @Value("${siteServer.priceboost.simplefilter.value}")
  private String hasPriceStreamValue;

  @Value("${siteServer.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteServer.priceboost.simplefilter.key}")
  private String hasPriceStreamKey;

  @Value("${market.template.winOrEachWayNextRaces}")
  private String[] winOrEachWayNextRaces;

  public SimpleFilter getClassSimpleFilter(String classIds) {
    return (SimpleFilter) createActiveByCategorySimpleFilter(classIds).build();
  }

  public static SimpleFilter getClassWithOpenEventsSimpleFilter(String classIds) {
    SimpleFilter.SimpleFilterBuilder builder = createActiveByCategorySimpleFilter(classIds);
    builder.addField(Clazz.HAS_OPEN_EVENT);
    return (SimpleFilter) builder.build();
  }

  public static SimpleFilter.SimpleFilterBuilder createActiveByCategorySimpleFilter(
      String classIds) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField(Clazz.IS_ACTIVE);
    builder.addBinaryOperation(Clazz.CATEGORY_ID, BinaryOperation.intersects, classIds);
    builder.addBinaryOperation(Clazz.SITE_CHANNELS, BinaryOperation.contains, "M");
    return builder;
  }

  public ExistsFilter getClassExistingFilter() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    builder.addBinaryOperation(
        "class:simpleFilter:event.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation(
        "class:simpleFilter:event.drilldownTagNames", BinaryOperation.intersects, EVFLAG_BL);
    return builder.build();
  }

  public static ExistsFilter getClassExistingFilterVirtuaHub() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    builder.addBinaryOperation(
        "class:simpleFilter:event.siteChannels", BinaryOperation.contains, "M");
    return builder.build();
  }

  public static ExistsFilter getEmptyExistingFilter() {
    return new ExistsFilter.ExistsFilterBuilder().build();
  }

  public ExistsFilter getEventToOutcomeForClassExistingFilter(
      boolean filterOutcomeMeaningMajorCode) {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    if (filterOutcomeMeaningMajorCode) {
      builder.addBinaryOperation(
          "market:simpleFilter:outcome.outcomeMeaningMajorCode", BinaryOperation.in, "HH,MR,H1");
    }
    builder.addField("event:simpleFilter:market.isMarketBetInRun");
    builder.addUnaryOperation("event:simpleFilter:market.isResulted", UnaryOperation.isFalse);
    builder.addField("event:simpleFilter:market.isDisplayed");
    return builder.build();
  }

  public ExistsFilter getEventToOutcomeForAllActiveMarkets() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    builder.addField("event:simpleFilter:market.isMarketBetInRun");
    builder.addUnaryOperation("event:simpleFilter:market.isResulted", UnaryOperation.isFalse);
    builder.addField("event:simpleFilter:market.isDisplayed");
    return builder.build();
  }

  public static ExistsFilter getNotSpecialEventsExistFilter() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    builder.addField("event:simpleFilter:market.drilldownTagNames:notIntersects:MKTFLAG_SP");
    return builder.build();
  }

  public SimpleFilter getLiveOrUpcomingEventToOutcomeByHRPrimMarket(String primaryMarkets) {
    SimpleFilter.SimpleFilterBuilder builder = getLiveOrUpcomingEventToOutcomeHRFilterBuilder();
    builder.addBinaryOperation(Market.NAME, BinaryOperation.in, primaryMarkets);
    builder.addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled);
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getLiveOrUpcomingEventToOutcomeByPrimMarket(String primaryMarkets) {
    SimpleFilter.SimpleFilterBuilder builder = getLiveOrUpcomingEventToOutcomeFilterBuilder();
    builder.addBinaryOperation(Market.NAME, BinaryOperation.in, primaryMarkets);
    builder.addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled);
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getEventToOutcomeForClassFilterExcludeTemplate(String outrightMarketName) {
    SimpleFilter.SimpleFilterBuilder builder = getLiveOrUpcomingEventToOutcomeFilterBuilder();
    builder.addBinaryOperation(
        Market.TEMPLATE_MARKET_NAME, BinaryOperation.notIntersects, outrightMarketName);
    builder.addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled);
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getEventToOutcomeForClassFilterWithMarketTemlates(String outrightMarketName) {
    SimpleFilter.SimpleFilterBuilder builder = getLiveOrUpcomingEventToOutcomeFilterBuilder();
    builder.addBinaryOperation(
        Market.TEMPLATE_MARKET_NAME, BinaryOperation.intersects, outrightMarketName);
    builder.addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled);
    return (SimpleFilter) builder.build();
  }

  public LimitToFilter getLowestMarketDisplayOrderLimitFilter() {
    LimitToFilter.LimitToFilterBuilder builder = new LimitToFilter.LimitToFilterBuilder();
    builder.addFieldWithLowestRank(Market.DISPLAY_ORDER);
    return builder.build();
  }

  public static LimitToFilter getEmptyLimitFilter() {
    return new LimitToFilter.LimitToFilterBuilder().build();
  }

  public static LimitRecordsFilter getEmptyLimitRecordsFilter() {
    return new LimitRecordsFilter.LimitRecordsFilterBuilder().build();
  }

  public static LimitRecordsFilter getMarketOutcomesLimitRecordsFilter(
      int marketsCount, int outcomesCount) {
    LimitRecordsFilter.LimitRecordsFilterBuilder builder =
        new LimitRecordsFilter.LimitRecordsFilterBuilder();
    builder.addField("market", marketsCount);
    builder.addField("outcome", outcomesCount);
    return builder.build();
  }

  public SimpleFilter getHRMarketCountForLiveOrUpcomingEventSimpleFilter() {
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(Event.TYPE_NAME, BinaryOperation.notEquals, ENHANCED_MULTIPLES);
    builder.addBinaryOperation(Event.SITE_CHANNELS, BinaryOperation.contains, "M");
    builder.addBinaryOperation(Market.SITE_CHANNELS, BinaryOperation.contains, "M");
    addHRBetInPlayListPredicate(builder);
    addStartTimePredicate(
        builder,
        ZonedDateTime.now(GMT_ZONE_ID).minusMinutes(Integer.parseInt(iHRMaxMinutes)),
        ZonedDateTime.now(GMT_ZONE_ID).plusHours(UPCOMING_EVENT_MAX_HOURS));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getMarketCountForLiveOrUpcomingEventSimpleFilter() {
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(Event.TYPE_NAME, BinaryOperation.notEquals, ENHANCED_MULTIPLES);
    builder.addBinaryOperation(Event.SITE_CHANNELS, BinaryOperation.contains, "M");
    builder.addBinaryOperation(Market.SITE_CHANNELS, BinaryOperation.contains, "M");
    addBetInPlayListPredicate(builder);
    addStartTimePredicate(
        builder,
        ZonedDateTime.now(GMT_ZONE_ID).minusDays(LIVE_EVENT_MAX_DAYS),
        ZonedDateTime.now(GMT_ZONE_ID).plusHours(UPCOMING_EVENT_MAX_HOURS));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return (SimpleFilter) builder.build();
  }

  public static SimpleFilter getRacingEventByTypeFlagsWithStartTimeUntil(
      String typeFlags,
      String excludeTypeFlags,
      Duration startTimeRange,
      String marketTemplateName) {
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(Event.EVENT_TYPE_FLAGCODES, BinaryOperation.intersects, typeFlags)
            .addBinaryOperation(
                Event.EVENT_TYPE_FLAGCODES, BinaryOperation.notIntersects, excludeTypeFlags)
            .addBinaryOperation(EVENT_DRILLDOWN_TAGNAMES, BinaryOperation.notContains, "EVFLAG_AP")
            .addBinaryOperation(
                "market.drilldownTagNames", BinaryOperation.notContains, "MKTFLAG_SP")
            .addBinaryOperation(
                Market.TEMPLATE_MARKET_NAME, BinaryOperation.intersects, marketTemplateName);

    addMobileChannelPredicate(builder);
    ZonedDateTime today = LocalDate.now().atStartOfDay().atZone(GMT_ZONE_ID);
    addStartTimePredicate(builder, today, today.plus(startTimeRange));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));

    return (SimpleFilter) builder.build();
  }

  public static SimpleFilter getToteEventBySelectionTimeRange(Duration startTimeRange) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    ZonedDateTime today = LocalDate.now().atStartOfDay(GMT_ZONE_ID);
    addStartTimePredicate(builder, today, today.plus(startTimeRange));
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getFilterForOutrightEvents() {
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(Event.SITE_CHANNELS, BinaryOperation.contains, "M")
            .addUnaryOperation(Event.IS_RESULTED, UnaryOperation.isFalse)
            .addBinaryOperation(
                OutrightsMarketConstants.EVENT_EVENTSORTCODE,
                BinaryOperation.intersects,
                OutrightsMarketConstants.OUTRIGHT_CODES);
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getFilterForNotStartedEvents() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    builder.addField("event.isStarted:isFalse");
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getFilterForFootballEvents(String displayMarketType) {
    Collection<MarketTemplateType> primaryMarkets = FOOTBALL.getPrimaryMarkets();
    if (Market.TWO_UP_MARKET.equals(displayMarketType))
      primaryMarkets.add(MarketTemplateType.TWO_UP_RESULT);
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(MARKET_DISP_SORT_NAME, BinaryOperation.intersects, MR_HH_3_W_2_W)
            .addBinaryOperation(Event.CATEGORY_CODE, BinaryOperation.equals, FOOTBALL.getSport())
            .addUnaryOperation(Event.IS_RESULTED, UnaryOperation.isFalse)
            .addBinaryOperation(
                Market.NAME, BinaryOperation.intersects, marketsAsString(primaryMarkets));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return (SimpleFilter) builder.build();
  }

  // process all markets for virtual events
  public SimpleFilter getFilterForVirtualEvents() {
    Collection<MarketTemplateType> primaryMarkets = VIRTUAL_EVENTS.getPrimaryMarkets();

    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
            .addUnaryOperation("event.isLiveNowEvent", UnaryOperation.isFalse)
            .addBinaryOperation(
                Event.CATEGORY_CODE, BinaryOperation.equals, VIRTUAL_EVENTS.getSport())
            .addUnaryOperation(Event.IS_RESULTED, UnaryOperation.isFalse)
            .addBinaryOperation(
                Market.NAME, BinaryOperation.intersects, marketsAsString(primaryMarkets));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter getFilterForNonFootballEvents() {
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(MARKET_DISP_SORT_NAME, BinaryOperation.intersects, MR_HH_3_W_2_W)
            .addBinaryOperation(Event.CATEGORY_CODE, BinaryOperation.notEquals, FOOTBALL.getSport())
            .addUnaryOperation(Event.IS_RESULTED, UnaryOperation.isFalse)
            .addBinaryOperation(
                Market.TEMPLATE_MARKET_NAME,
                BinaryOperation.intersects,
                marketsAsString(NON_FOOTBALL.getPrimaryMarkets()));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return (SimpleFilter) builder.build();
  }

  private SimpleFilter.SimpleFilterBuilder getLiveOrUpcomingEventToOutcomeHRFilterBuilder() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField(Market.IS_BET_IN_RUN);
    addMobileChannelPredicate(builder);
    addHRBetInPlayListPredicate(builder);
    addStartTimePredicate(
        builder,
        ZonedDateTime.now(GMT_ZONE_ID).minusMinutes(Integer.parseInt(iHRMaxMinutes)),
        ZonedDateTime.now(GMT_ZONE_ID).plusHours(UPCOMING_EVENT_MAX_HOURS));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return builder;
  }

  private static SimpleFilter.SimpleFilterBuilder getLiveOrUpcomingEventToOutcomeFilterBuilder() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField(Market.IS_BET_IN_RUN);
    addMobileChannelPredicate(builder);
    addBetInPlayListPredicate(builder);
    addStartTimePredicate(
        builder,
        ZonedDateTime.now(GMT_ZONE_ID).minusDays(LIVE_EVENT_MAX_DAYS),
        ZonedDateTime.now(GMT_ZONE_ID).plusHours(UPCOMING_EVENT_MAX_HOURS));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    return builder;
  }

  public SimpleFilter getLiveFootballEventToOutcomeForClassFilter() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    addMobileChannelPredicate(builder);
    addBetInPlayListPredicate(builder);
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    builder.addBinaryOperation("event.rawIsOffCode", BinaryOperation.equals, "Y");
    builder.addField("market.isMarketBetInRun");
    builder.addField("event.isStarted");
    builder.addField("event.isLiveNowEvent");
    builder.addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled);
    return (SimpleFilter) builder.build();
  }

  public static SimpleFilter getNextRaces(String excludeTypeIds) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();

    builder.addBinaryOperation(Event.SITE_CHANNELS, BinaryOperation.contains, "M");
    builder.addUnaryOperation(Event.IS_FINISHED, UnaryOperation.isFalse);
    builder.addBinaryOperation(Event.TYPE_ID, BinaryOperation.notIn, excludeTypeIds);

    return (SimpleFilter) builder.build();
  }

  public static SimpleFilter getPoolTypesPredicate(List<String> poolTypes) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation(
        "pool.type", BinaryOperation.intersects, String.join(",", poolTypes));
    return (SimpleFilter) builder.build();
  }

  private static void addMobileChannelPredicate(SimpleFilter.SimpleFilterBuilder builder) {
    builder.addBinaryOperation(Event.SITE_CHANNELS, BinaryOperation.contains, "M");
    builder.addBinaryOperation(Market.SITE_CHANNELS, BinaryOperation.contains, "M");
    builder.addBinaryOperation("outcome.siteChannels", BinaryOperation.contains, "M");
  }

  private static void addBetInPlayListPredicate(SimpleFilter.SimpleFilterBuilder builder) {
    builder.addBinaryOperation(EVENT_DRILLDOWN_TAGNAMES, BinaryOperation.intersects, EVFLAG_BL);
  }

  private static void addHRBetInPlayListPredicate(SimpleFilter.SimpleFilterBuilder builder) {
    builder.addBinaryOperation(EVENT_DRILLDOWN_TAGNAMES, BinaryOperation.intersects, EVFLAG_IHR);
  }

  private static void addStartTimePredicate(
      SimpleFilter.SimpleFilterBuilder builder, ZonedDateTime fromDate, ZonedDateTime toDate) {
    builder.addBinaryOperation(
        Event.START_TIME,
        BinaryOperation.greaterThanOrEqual,
        DateTimeHelper.toString(trimToTenSeconds(fromDate.toLocalDateTime())));
    builder.addBinaryOperation(
        Event.START_TIME,
        BinaryOperation.lessThanOrEqual,
        DateTimeHelper.toString(trimToTenSeconds(toDate.toLocalDateTime())));
  }

  private static void addSuspendTimePredicate(
      SimpleFilter.SimpleFilterBuilder builder, ZonedDateTime afterTime) {
    builder.addBinaryOperation(
        Event.SUSPEND_AT_TIME,
        BinaryOperation.greaterThan,
        DateTimeHelper.toString(trimToTenSeconds(afterTime.toLocalDateTime())));
  }

  private String marketsAsString(Collection<MarketTemplateType> primaryMarkets) {
    return marketTemplateNameService.asQuery(primaryMarkets);
  }

  public SimpleFilter getActiveClassesForTheCategory(String classIds) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField(Clazz.IS_ACTIVE);
    builder.addField(Clazz.HAS_OPEN_EVENT);
    builder.addBinaryOperation(Clazz.CATEGORY_ID, BinaryOperation.equals, classIds);
    builder.addBinaryOperation(Clazz.SITE_CHANNELS, BinaryOperation.contains, "M");
    return (SimpleFilter) builder.build();
  }

  public SimpleFilter buildSimpleFilterForNextRaces(String typeFlagCodes) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation(
        Event.EVENT_TYPE_FLAGCODES, BinaryOperation.intersects, typeFlagCodes);
    builder.addField("event.isActive:isTrue");
    builder.addBinaryOperation(Event.SITE_CHANNELS, BinaryOperation.contains, "M");
    builder.addBinaryOperation("event.eventStatusCode", BinaryOperation.equals, "A");
    builder.addBinaryOperation("event.rawIsOffCode", BinaryOperation.notEquals, "Y");
    builder.addField("event.isStarted:isFalse");
    builder.addBinaryOperation(Event.START_TIME, BinaryOperation.greaterThanOrEqual, Instant.now());
    builder.addBinaryOperation(
        Market.TEMPLATE_MARKET_NAME,
        BinaryOperation.intersects,
        asQueryFromMarketStrings(winOrEachWayNextRaces));
    builder.addBinaryOperation(Market.MARKET_STATUS_CODE, BinaryOperation.equals, "A");
    builder.addBinaryOperation("outcome.outcomeStatusCode", BinaryOperation.equals, "A");
    builder.addBinaryOperation("outcome.outcomeMeaningMinorCode", BinaryOperation.notEquals, "1");
    builder.addBinaryOperation("outcome.outcomeMeaningMinorCode", BinaryOperation.notEquals, "2");
    return (SimpleFilter) builder.build();
  }

  public String asQueryFromMarketStrings(String[] primaryMarkets) {
    return marketTemplateNameService.asQueryFromMarketStrings(primaryMarkets);
  }

  public ExistsFilter buildExistsFilterForNextRaces() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    builder.addBinaryOperation(
        "event:simpleFilter:market.marketStatusCode", BinaryOperation.equals, "A");
    return builder.build();
  }

  public LimitRecordsFilter buildLimitRecordsFilterForNextRaces() {
    LimitRecordsFilter.LimitRecordsFilterBuilder builder =
        new LimitRecordsFilter.LimitRecordsFilterBuilder();
    builder.addField("outcome", OUTCOME_LIMIT);
    return builder.build();
  }

  private static class Event {
    static final String SITE_CHANNELS = "event.siteChannels";
    static final String CATEGORY_CODE = "event.categoryCode";
    static final String IS_RESULTED = "event.isResulted";
    static final String IS_FINISHED = "event.isFinished";
    static final String START_TIME = "event.startTime";
    static final String SUSPEND_AT_TIME = "event.suspendAtTime";
    static final String TYPE_NAME = "event.typeName";
    static final String TYPE_ID = "event.typeId";
    static final String EVENT_TYPE_FLAGCODES = "event.typeFlagCodes";
  }

  private static class Market {
    static final String IS_BET_IN_RUN = "market.isMarketBetInRun";
    static final String SITE_CHANNELS = "market.siteChannels";
    static final String NAME = "market.name";
    static final String TEMPLATE_MARKET_NAME = "market.templateMarketName";

    static final String MARKET_STATUS_CODE = "market.marketStatusCode";
    static final String DISPLAY_ORDER = "market.displayOrder";
    static final String TWO_UP_MARKET = "2UpMarket";
  }

  private static class Clazz {
    static final String CATEGORY_ID = "class.categoryId";
    static final String IS_ACTIVE = "class.isActive";
    static final String HAS_OPEN_EVENT = "class.hasOpenEvent";
    static final String SITE_CHANNELS = "class.siteChannels";
  }

  /** Created constants for outright markets to resolve the SONAR issues. */
  private static class OutrightsMarketConstants {
    static final String OUTRIGHT_CODES =
        "TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20";
    static final String EVENT_EVENTSORTCODE = "event.eventSortCode";
  }
}
