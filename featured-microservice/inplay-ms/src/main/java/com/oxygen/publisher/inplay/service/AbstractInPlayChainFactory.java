package com.oxygen.publisher.inplay.service;

import com.oxygen.publisher.model.InPlayByEventMarket;
import com.oxygen.publisher.model.ModuleDataItem;
import com.oxygen.publisher.model.OutputMarket;
import com.oxygen.publisher.model.RawIndex;
import com.oxygen.publisher.translator.ChainFactory;
import java.util.*;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.util.CollectionUtils;

/** Created by Aliaksei Yarotski on 4/13/18. */
@Slf4j
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public abstract class AbstractInPlayChainFactory implements ChainFactory {

  public static final String MAIN_MARKET = "Main Market";
  public static final String CURRENT_SET_WINNER = "Current Set Winner";
  protected static final List<String> SPORT_CATEGORY_WITH_SETRESULT = Arrays.asList("34");

  protected static List<ModuleDataItem> optimizeEvents(
      Map<String, InPlayByEventMarket> prMarketsCache,
      List<ModuleDataItem> events,
      RawIndex rawIndex) {
    if (events == null) {
      return Collections.emptyList();
    }
    return events.stream()
        .map(event -> optimizeEvent(event, rawIndex, prMarketsCache))
        .collect(Collectors.toList());
  }

  private static ModuleDataItem optimizeEvent(
      ModuleDataItem event, RawIndex rawIndex, Map<String, InPlayByEventMarket> prMarketsCache) {
    if (CollectionUtils.isEmpty(event.getMarkets())) {
      log.info(
          "No markets for {} event by cache ref: {}. Primary markets count: {}.",
          event.getId(),
          rawIndex.toStructuredKey(),
          event.getPrimaryMarkets() == null ? 0 : event.getPrimaryMarkets().size());
    } else {
      cropMarkets(rawIndex, event);
      logInconsistencyMarketsCheck(rawIndex, event);
      updateEventMarketInCache(prMarketsCache, rawIndex, event);
    }
    event.setPrimaryMarkets(null);
    return event;
  }

  private static void updateEventMarketInCache(
      Map<String, InPlayByEventMarket> prMarketsCache, RawIndex rawIndex, ModuleDataItem event) {
    String eventKey = createPRMarketCacheIndex(event.getId(), event.getMarkets());
    InPlayByEventMarket eventMarket =
        prMarketsCache.computeIfAbsent(eventKey, e -> new InPlayByEventMarket());
    eventMarket.addCacheRef(rawIndex);
    eventMarket.setModuleDataItem(event);
    eventMarket.setPrimaryMarkets(event.getPrimaryMarkets());
    log.debug("{} ------> {} ", rawIndex.toStructuredKey(), eventKey);
  }

  /**
   * BMA-29428: Market selector shows Match result market for not Match Betting market.
   *
   * @param rawIndex - inplay cache key index representation.
   * @param event - event.
   */
  private static void logInconsistencyMarketsCheck(RawIndex rawIndex, ModuleDataItem event) {
    if (log.isDebugEnabled()
        && rawIndex.getMarketSelector() != null
        && StringUtils.compareIgnoreCase(
                rawIndex.getMarketSelector().trim(),
                event.getMarkets().get(0).getTemplateMarketName().trim())
            != 0) {

      log.error(
          "EventId: {} Expected market: {} Actual market: {}",
          event.getId(),
          rawIndex.getMarketSelector(),
          event.getMarkets().get(0).getName());
    }
  }

  /**
   * BMA-29278: for case with duplication by market template name.
   *
   * @param rawIndex index.
   * @param event event list.
   */
  protected static void cropMarkets(RawIndex rawIndex, ModuleDataItem event) {
    if ((rawIndex.getMarketSelector() == null || rawIndex.getMarketSelector().equals(MAIN_MARKET))
        && !CollectionUtils.isEmpty(event.getPrimaryMarkets())) {
      log.debug(
          "BMA-29278 set correct main market: EventId#{} Index#{}",
          event.getId(),
          rawIndex.toStructuredKey());
      event.setMarkets(Collections.singletonList(event.getPrimaryMarkets().get(0)));
    } else if (event.getMarkets() != null && event.getMarkets().size() > 1) {
      log.debug(
          "BMA-29278 set correct market: EventId#{} Index#{}",
          event.getId(),
          rawIndex.toStructuredKey());
      event.setMarkets(
          SPORT_CATEGORY_WITH_SETRESULT.contains(event.getCategoryId())
                  && rawIndex.getMarketSelector().equals(CURRENT_SET_WINNER)
                  && event.getComments() != null
              ? getLowestDisplayNumberCorrectSetResult(
                  event.getMarkets(), event.getComments().getRunningSetIndex())
              : geLowestDisplayNumberMarket(event.getMarkets()));
    }
  }

  // as per BMA-50078, we should take only lowest dispNumber market
  private static List<OutputMarket> geLowestDisplayNumberMarket(List<OutputMarket> markets) {
    return Collections.singletonList(
        markets.stream()
            .min(Comparator.nullsLast(Comparator.comparing(OutputMarket::getDisplayOrder)))
            .orElse(markets.get(0)));
  }

  private static List<OutputMarket> getLowestDisplayNumberCorrectSetResult(
      List<OutputMarket> markets, Integer runInSetIndex) {
    String setXResult = String.format("Set %s Result", runInSetIndex);
    return Collections.singletonList(
        markets.stream()
            .sorted(Comparator.nullsLast(Comparator.comparing(OutputMarket::getDisplayOrder)))
            .filter(market -> setXResult.equalsIgnoreCase(market.getName()))
            .findFirst()
            .orElse(markets.get(0)));
  }

  protected static String getNextPrimaryMarketId(InPlayByEventMarket cachedEvent) {
    ModuleDataItem thisEvent = cachedEvent.getModuleDataItem();
    OutputMarket oldMarket = thisEvent.getMarkets().get(0);
    int index = cachedEvent.getPrimaryMarkets().indexOf(oldMarket);
    if (index < 0 || cachedEvent.getPrimaryMarkets().size() < index + 2) {
      log.info(
          "[ AbstractInPlayChainFactory:matchNextPrimaryMarket ] {}->{} not found in the "
              + "primary market collection. ",
          thisEvent.getId(),
          oldMarket.getId());
      return null;
    }
    return cachedEvent.getPrimaryMarkets().get(index + 1).getId();
  }

  public static String createPRMarketCacheIndex(String eventId, String marketId) {
    return eventId + "::" + marketId;
  }

  public static String createPRMarketCacheIndex(Integer eventId, List<OutputMarket> markets) {

    String index = eventId.toString();
    if (markets == null || markets.isEmpty()) {
      return index + "::";
    }
    return createPRMarketCacheIndex(index, markets.get(0).getId());
  }
}
