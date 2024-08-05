package com.entain.oxygen.util;

import com.egalacoral.spark.siteserver.api.*;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import lombok.experimental.UtilityClass;

@UtilityClass
public class FilterUtil {

  private static final String EVENT_SITE_CHANNELS = "event.siteChannels";
  private static final String EVENT_START_TIME = "event.startTime";
  private static final String TEMPLATE_MARKET_NAME = "market.templateMarketName";
  private static final String EVENT_IS_RESULTED = "event.isResulted";
  private static final String EVENT_TYPE_FLAG_CODES = "event.typeFlagCodes";
  private static final String UK_IE_FLAG_CODES = "UK,IE";
  private static final String MARKET_NAMES = "|Win or Each Way|,|Outright|";
  public static final String EVENT_STATUS_CODE = "event.eventStatusCode";

  private static Instant nowUtcWithoutMillis() {
    return Instant.now().truncatedTo(ChronoUnit.SECONDS);
  }

  public SimpleFilter.SimpleFilterBuilder buildSimpleFilterForUKIEHorses() {
    return new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addBinaryOperation(
            EVENT_START_TIME, BinaryOperation.greaterThanOrEqual, nowUtcWithoutMillis())
        .addBinaryOperation(EVENT_TYPE_FLAG_CODES, BinaryOperation.intersects, UK_IE_FLAG_CODES)
        .addBinaryOperation(EVENT_STATUS_CODE, BinaryOperation.equals, "A")
        .addUnaryOperation(EVENT_IS_RESULTED, UnaryOperation.isFalse)
        .addBinaryOperation(TEMPLATE_MARKET_NAME, BinaryOperation.intersects, MARKET_NAMES);
  }

  public LimitToFilter limitToFilter() {
    return new LimitToFilter.LimitToFilterBuilder().build();
  }

  public ExistsFilter existsFilter() {
    return new ExistsFilter.ExistsFilterBuilder().build();
  }

  public LimitRecordsFilter limitRecordsFilter() {
    return new LimitRecordsFilter.LimitRecordsFilterBuilder().build();
  }
}
