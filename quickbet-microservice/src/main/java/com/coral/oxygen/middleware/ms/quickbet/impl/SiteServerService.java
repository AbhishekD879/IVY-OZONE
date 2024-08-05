package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.util.JavaDateUtils;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Scorecast;
import io.vavr.collection.List;
import java.util.Optional;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Component;

/** Created by azayats on 07.12.17. */
@Component
public class SiteServerService {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private static final String TIME_ZONE = "GMT";
  private final SiteServerApi siteServerApi;
  private final int akamaiCacheTtl;

  @Value("${siteserver.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteserver.priceboost.simplefilter.key}")
  private String priceBoostSimpleFilterKey;

  @Value("${siteserver.priceboost.simplefilter.value}")
  private String priceBoostSimpleFilterValue;

  @Autowired
  public SiteServerService(
      SiteServerApi siteServerApi, @Value("${siteserve.timequery.seconds}") int akamaiCacheTtl) {
    this.siteServerApi = siteServerApi;
    this.akamaiCacheTtl = akamaiCacheTtl;
  }

  public List<Event> getEventsForOutcomeIds(List<String> outcomeIds) {

    return getEventsFor(outcomeIds.toJavaList()).map(List::ofAll).orElseGet(List::empty);
  }

  public Optional<java.util.List<Event>> getEventToOutcomeForOutcome(
      java.util.List<Long> outcomeIds) {
    return getEventsFor(outcomeIds.stream().map(String::valueOf).toList());
  }

  @Cacheable(cacheNames = "outcomeData")
  public Optional<java.util.List<Event>> getEventsFor(java.util.List<String> outcomeIds) {
    ASYNC_LOGGER.info(
        "[getEventsFor] making a siteserv call to get events with outcome ids:: {}", outcomeIds);
    return siteServerApi.getEventToOutcomeForOutcome(
        outcomeIds,
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation(
                    "event.suspendAtTime",
                    BinaryOperation.greaterThan,
                    JavaDateUtils.reformatToSeconds(
                        DateTime.now(DateTimeZone.forID(TIME_ZONE)), akamaiCacheTtl))
                .addPriceStream(
                    priceBoostSimpleFilterKey, priceBoostSimpleFilterValue, isPriceBoostEnabled)
                .build(),
        null,
        false);
  }

  @Cacheable(cacheNames = "scorecastData")
  public Optional<Scorecast> getScorecast(String marketId, String scorerOutcomeId) {
    return siteServerApi.getScorecast(marketId, scorerOutcomeId);
  }

  public Optional<java.util.List<Event>> getEventToOutcomeForMarketForLuckyDip(String marketId) {
    ASYNC_LOGGER.info(
        "[getEventsFor] making a siteserv call to get events with marketId:: {}", marketId);
    return siteServerApi.getWholeEventToOutcomeForMarket(
        marketId,
        true,
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
                .build());
  }
}
