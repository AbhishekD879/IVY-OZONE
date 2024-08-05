package com.egalacoral.spark.siteserver.api;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Arrays;
import java.util.Collections;

public class TypeWithLimitSpec {

  public void test() throws NoSuchAlgorithmException, KeyManagementException {
    SiteServerApi siteServerApi =
        new SiteServerImpl.Builder()
            .setUrl("https://ss-aka-ori.coral.co.uk/")
            .setMaxNumberOfRetries(2)
            .setReadTimeout(2)
            .build();

    siteServerApi.getEventToOutcomeForType(
        Collections.singletonList("442"),
        getSimpleFilterForNextEventsByType(),
        getExistedFilterForNextEventsByType(),
        getEventToOutcomeForClassLimitFilter(),
        Collections.singletonList("event"),
        false);

    siteServerApi.getEventToOutcomeForEvent(
        Arrays.asList("10238503", "9216860"),
        getSimpleFilterForNextEventsByType(),
        getExistedFilterForNextEventsByType(),
        getEventToOutcomeForClassLimitFilter(),
        getEventToOutcomeForClassLimitRecordsFilter(),
        Collections.singletonList("event"),
        false);
  }

  private SimpleFilter getSimpleFilterForNextEventsByType() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation("outcome.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation(
        "market.templateMarketName",
        BinaryOperation.in,
        "|Match Betting|,|Both Teams to Score|,|Over/Under Total Goals|,|Draw No Bet|,|To Win Not to Nil|,|First-Half Result|,|Next Team to Score|,|To Qualify|,|Extra-Time Result|");
    builder.addUnaryOperation("event.isStarted", UnaryOperation.isFalse);
    builder.addBinaryOperation(
        "event.suspendAtTime",
        BinaryOperation.greaterThan,
        Instant.now().truncatedTo(ChronoUnit.MINUTES));
    return (SimpleFilter) builder.build();
  }

  private ExistsFilter getExistedFilterForNextEventsByType() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();

    builder.addUnaryOperation("event:simpleFilter:market.isResulted", UnaryOperation.isFalse);
    builder.addField("event:simpleFilter:market.isDisplayed");
    return builder.build();
  }

  private LimitToFilter getEventToOutcomeForClassLimitFilter() {
    LimitToFilter.LimitToFilterBuilder builder = new LimitToFilter.LimitToFilterBuilder();
    builder.addFieldWithLowestRank("market.displayOrder");
    return builder.build();
  }

  private LimitRecordsFilter getEventToOutcomeForClassLimitRecordsFilter() {
    LimitRecordsFilter.LimitRecordsFilterBuilder builder =
        new LimitRecordsFilter.LimitRecordsFilterBuilder();
    builder.addField("outcome", 2);
    return builder.build();
  }
}
