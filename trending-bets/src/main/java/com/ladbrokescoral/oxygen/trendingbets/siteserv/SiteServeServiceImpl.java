package com.ladbrokescoral.oxygen.trendingbets.siteserv;

import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputMarket;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputOutcome;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.EventToTrendingEventConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.MarketToOutputMarketConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.OutcomeToOutputOutcomeConverter;
import com.ladbrokescoral.oxygen.trendingbets.util.TrendingBetsUtil;
import java.util.*;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.Mono;

@Slf4j
@Service
@RequiredArgsConstructor
public abstract class SiteServeServiceImpl implements SiteServeService {

  protected static final String FZ_MARKET = "MKTFLAG_FZ";

  private final SiteServerApiAsync siteServerApiAsync;

  private final EventToTrendingEventConverter eventToTrendingEventConverter;
  private final MarketToOutputMarketConverter marketToOutputMarketConverter;
  private final OutcomeToOutputOutcomeConverter outcomeToOutputOutcomeConverter;

  @Value("${popularbets.hide.market.drilldownTagNames}")
  private String[] marketDrilldownTagNames;

  @Value("${popularbets.hide.event.drilldownTagNames}")
  private String[] eventDrilldownTagNames;

  /**
   * Makes SiteServe call for the received TrendingItems if it is not present in the
   * TrendingBetsContext with given selectionId. If already exist, then corresponding TrendingEvent
   * will be mapped.
   *
   * <p>If any selection is invalid w.r.t siteserve data, then corresponding entry will be removed
   * from trendingItems list.
   *
   * @param trendingItems
   * @return Mono of trendingItems
   */
  public Mono<List<TrendingItem>> getEventToOutcomeForOutcome(List<TrendingItem> trendingItems) {

    Map<String, List<TrendingItem>> outcomesIdsMap = generateOutcomeMap(trendingItems);

    if (CollectionUtils.isEmpty(outcomesIdsMap.keySet())) return Mono.just(trendingItems);

    SimpleFilter simpleFilter = getSimpleFilter();
    List<String> prune = new ArrayList<>();
    prune.add("event");
    prune.add("market");

    return siteServerApiAsync
        .getEventToOutcomeForOutcome(
            List.copyOf(outcomesIdsMap.keySet()), simpleFilter, prune, false)
        .map(
            (List<Event> events) -> {
              events.forEach(event -> updateSiteServerData(outcomesIdsMap, event));
              // remove All invalid items with  no resposne from Siteserv call with selection ID
              if (!outcomesIdsMap.keySet().isEmpty())
                log.info("invalid selection ids are :: {}", outcomesIdsMap.keySet());
              trendingItems.removeAll(
                  outcomesIdsMap.values().stream().flatMap(Collection::stream).toList());
              return trendingItems;
            });
  }

  protected SimpleFilter getSimpleFilter() {
    return (SimpleFilter)
        new SimpleFilter.SimpleFilterBuilder()
            .addUnaryOperation("event.liveServChannels", UnaryOperation.isNotEmpty)
            .build();
  }

  private Map<String, List<TrendingItem>> generateOutcomeMap(List<TrendingItem> trendingItems) {
    return trendingItems.stream()
        .map(this::updateLivesChannels)
        .filter(trendingItem -> trendingItem.getTrendingEvent() == null)
        .collect(Collectors.groupingBy(TrendingItem::getSelectionId));
  }

  private TrendingItem updateLivesChannels(TrendingItem trendingItem) {
    List<TrendingEvent> tSelection = getTrendingSelection(trendingItem.getSelectionId());
    if (!CollectionUtils.isEmpty(tSelection)) {
      TrendingEvent selection = tSelection.get(0);
      trendingItem.setSelectionLivesChannel(
          selection.getMarkets().get(0).getOutcomes().get(0).getLiveServChannels());
      trendingItem.setTrendingEvent(selection);
    }
    return trendingItem;
  }

  protected abstract List<TrendingEvent> getTrendingSelection(String selectionId);

  private void updateSiteServerData(Map<String, List<TrendingItem>> outcomesIdsMap, Event event) {
    event
        .getMarkets()
        .forEach(
            market ->
                market
                    .getOutcomes()
                    .forEach(
                        (Outcome outcome) -> {
                          outcomesIdsMap
                              .get(outcome.getId())
                              .forEach(item -> enrichTrendingItem(item, event, market, outcome));
                          outcomesIdsMap.remove(outcome.getId());
                        }));
  }

  /**
   * Updates TrendingItem with siteServe data.
   *
   * @param trendingItem
   * @param event
   * @param market
   * @param outcome
   */
  private void enrichTrendingItem(
      TrendingItem trendingItem, Event event, Market market, Outcome outcome) {
    trendingItem.setSelectionName(outcome.getName());
    trendingItem.setMarketName(market.getName());
    trendingItem.setEventName(event.getName());
    trendingItem.setIsStarted(Boolean.TRUE.equals(event.getIsStarted()));
    trendingItem.setEventDateTime(event.getStartTime());
    trendingItem.setMarketId(market.getId());
    trendingItem.setSuspended(
        !isActive(event.getIsActive(), market.getIsActive(), outcome.getIsActive()));
    trendingItem.setSelectionLivesChannel(
        outcome.getLiveServChannels().contains(",")
            ? outcome.getLiveServChannels().split(",")[0]
            : outcome.getLiveServChannels());
    TrendingEvent trendingEvent = eventToTrendingEventConverter.convert(event);
    OutputMarket outputMarket = marketToOutputMarketConverter.convert(market);
    OutputOutcome outputOutcome = outcomeToOutputOutcomeConverter.convert(outcome);
    outputMarket.setOutcomes(Arrays.asList(outputOutcome));
    trendingEvent.setMarkets(Arrays.asList(outputMarket));
    trendingEvent.setSelectionId(trendingItem.getSelectionId());
    trendingEvent.setIsSuspended(trendingItem.getSuspended());
    trendingEvent.setHideEventName(
        TrendingBetsUtil.checkDrillDownTagsMatch(
            trendingEvent, eventDrilldownTagNames, marketDrilldownTagNames));
    trendingItem.setTrendingEvent(trendingEvent);
  }

  private Boolean isActive(Boolean eventActive, Boolean marketActive, Boolean selectionActive) {
    return Boolean.TRUE.equals(eventActive)
        && Boolean.TRUE.equals(marketActive)
        && Boolean.TRUE.equals(selectionActive);
  }
}
