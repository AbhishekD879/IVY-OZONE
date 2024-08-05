package com.coral.oxygen.middleware.featured.service.injector;

import static com.coral.oxygen.middleware.common.service.DateTimeHelper.trimToTenSeconds;
import static com.coral.oxygen.middleware.common.utils.QueryFilterBuilder.getEmptyLimitRecordsFilter;

import com.coral.oxygen.middleware.common.service.DateTimeHelper;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class ConsumeBirHREvents {

  private static final String HR_CATEGORY_ID = "21";
  private static final String EVFLAG_BL = "EVFLAG_BL";
  private final SiteServerApi siteServerApi;
  private final MarketTemplateNameService marketTemplateNameService;
  public static final ZoneId GMT_ZONE_ID = ZoneId.of("GMT");
  private static final int LIVE_EVENT_MAX_DAYS = 5;
  private static final int UPCOMING_EVENT_MAX_HOURS = 24;
  private static final String EVFLAG_IHR = "EVFLAG_IHR";
  private static final String EVENT_DRILLDOWN_TAGNAMES = "event.drilldownTagNames";

  public static final String EVENT_EXTERNAL_KEYS_TYPE = "event";

  @Autowired
  public ConsumeBirHREvents(
      SiteServerApi siteServerApi, MarketTemplateNameService marketTemplateNameService) {
    this.siteServerApi = siteServerApi;
    this.marketTemplateNameService = marketTemplateNameService;
  }

  public List<Children> consumeBirEvents() {
    SimpleFilter simpleFilter = getClassSimpleFilter(HR_CATEGORY_ID);
    ExistsFilter existsFilter1 = classExistingFilter();
    List<Category> classes =
        siteServerApi.getClasses(simpleFilter, existsFilter1).orElse(Collections.emptyList());
    List<String> classIds =
        classes.stream()
            .map(c -> String.valueOf(c.getId()))
            .collect(Collectors.toCollection(ArrayList::new));
    SimpleFilter filter = getEventToOutcomeForClassSimpleFilter();
    LimitToFilter limitToFilter = new LimitToFilter.LimitToFilterBuilder().build();
    ExistsFilter existsFilter = new ExistsFilter.ExistsFilterBuilder().build();
    LimitRecordsFilter limitRecordsFilter = getEmptyLimitRecordsFilter();
    List<String> prune = Collections.emptyList();
    Optional<List<Children>> eventsOptional =
        siteServerApi.getEventToOutcomeForClass(
            classIds,
            filter,
            limitToFilter,
            limitRecordsFilter,
            existsFilter,
            prune,
            EVENT_EXTERNAL_KEYS_TYPE,
            true);
    log.info("ConsumeBirHREvents eventsOptional {}", eventsOptional);
    return eventsOptional.orElse(Collections.emptyList());
  }

  public SimpleFilter getClassSimpleFilter(String classIds) {
    return (SimpleFilter) activeByCategorySimpleFilter(classIds).build();
  }

  public static SimpleFilter.SimpleFilterBuilder activeByCategorySimpleFilter(String classIds) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField(Clazz.IS_ACTIVE);
    builder.addBinaryOperation(Clazz.CATEGORY_ID, BinaryOperation.intersects, classIds);
    builder.addBinaryOperation(Clazz.SITE_CHANNELS, BinaryOperation.contains, "M");
    return builder;
  }

  public ExistsFilter classExistingFilter() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    builder.addBinaryOperation(
        "class:simpleFilter:event.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation(
        "class:simpleFilter:event.drilldownTagNames", BinaryOperation.intersects, EVFLAG_BL);
    return builder.build();
  }

  private SimpleFilter getEventToOutcomeForClassSimpleFilter() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation(Event.SITE_CHANNELS, BinaryOperation.contains, "M");
    builder.addBinaryOperation(
        Event.EVENT_TYPE_FLAG_CODES, BinaryOperation.intersects, "UK,IE,INT");
    addStartTimePredicate(
        builder,
        ZonedDateTime.now(GMT_ZONE_ID).minusDays(LIVE_EVENT_MAX_DAYS),
        ZonedDateTime.now(GMT_ZONE_ID).plusHours(UPCOMING_EVENT_MAX_HOURS));
    builder.addBinaryOperation(
        Market.TEMPLATE_MARKET_NAME,
        BinaryOperation.intersects,
        marketTemplateNameService.asQuery(MarketTemplateType.WIN_OR_EACH_WAY));
    addSuspendTimePredicate(builder, ZonedDateTime.now(GMT_ZONE_ID));
    builder.addBinaryOperation(Event.RAW_IS_OFF_CODE, BinaryOperation.equals, "Y");
    builder.addBinaryOperation(Market.MARKET_STATUS_CODE, BinaryOperation.equals, "A");
    builder.addBinaryOperation(Event.STATUS_CODE, BinaryOperation.equals, "A");
    builder.addUnaryOperation(Event.IS_RESULTED, UnaryOperation.isFalse);
    builder.addBinaryOperation("outcome.outcomeMeaningMinorCode", BinaryOperation.notEquals, "1");
    builder.addBinaryOperation("outcome.outcomeMeaningMinorCode", BinaryOperation.notEquals, "2");
    builder.addBinaryOperation("outcome.outcomeStatusCode", BinaryOperation.equals, "A");
    addHRBetInPlayListPredicate(builder);
    return (SimpleFilter) builder.build();
  }

  private static void addHRBetInPlayListPredicate(SimpleFilter.SimpleFilterBuilder builder) {
    builder.addBinaryOperation(EVENT_DRILLDOWN_TAGNAMES, BinaryOperation.contains, EVFLAG_IHR);
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

  private static class Clazz {
    static final String CATEGORY_ID = "class.categoryId";
    static final String IS_ACTIVE = "class.isActive";
    static final String SITE_CHANNELS = "class.siteChannels";
  }

  private static class Event {
    static final String SITE_CHANNELS = "event.siteChannels";
    static final String RAW_IS_OFF_CODE = "event.rawIsOffCode";
    static final String IS_RESULTED = "event.isResulted";
    static final String START_TIME = "event.startTime";
    static final String SUSPEND_AT_TIME = "event.suspendAtTime";
    static final String STATUS_CODE = "event.eventStatusCode";
    static final String EVENT_TYPE_FLAG_CODES = "event.typeFlagCodes";
  }

  private static class Market {
    static final String TEMPLATE_MARKET_NAME = "market.templateMarketName";

    static final String MARKET_STATUS_CODE = "market.marketStatusCode";
  }
}
