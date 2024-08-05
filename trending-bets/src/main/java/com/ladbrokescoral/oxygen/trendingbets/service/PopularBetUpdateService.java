package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.domain.EventStatus;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.domain.MarketStatus;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.domain.SelectionStatus;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputMarket;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputOutcome;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputPrice;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.util.TrendingBetsUtil;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class PopularBetUpdateService {
  private static final int SCALE_VALUE = 2;

  public List<TrendingEvent> updateEvent(EventStatus eventStatus, String channel) {

    return getTrendingEvents(channel).stream()
        .map(
            (TrendingEvent trendingSelection) -> {
              Optional.ofNullable(eventStatus.getStarted())
                  .ifPresent(trendingSelection::setEventIsLive);
              Optional.ofNullable(eventStatus.getStartTime())
                  .ifPresent(
                      startTime ->
                          trendingSelection.setStartTime(
                              TrendingBetsUtil.convertToSiteServeTimeFormat(startTime)));
              Optional.ofNullable(eventStatus.getStatus())
                  .ifPresent(trendingSelection::setEventStatusCode);
              Optional.ofNullable(eventStatus.getDisplayed())
                  .ifPresent(
                      displayed ->
                          trendingSelection.setIsDisplayed("Y".equalsIgnoreCase(displayed)));
              updateSuspendStatus(trendingSelection);
              return trendingSelection;
            })
        .filter(trendingSelection -> Boolean.TRUE.equals(trendingSelection.getEventIsLive()))
        .toList();
  }

  public void updateMarket(MarketStatus marketStatus, String marketId) {

    getTrendingEvents(marketId)
        .forEach(
            (TrendingEvent trendingSelection) -> {
              OutputMarket market = trendingSelection.getMarkets().get(0);
              Optional.ofNullable(marketStatus.getStatus()).ifPresent(market::setMarketStatusCode);
              Optional.ofNullable(marketStatus.getDisplayed())
                  .ifPresent(displayed -> market.setIsDisplayed("Y".equalsIgnoreCase(displayed)));
              updateSuspendStatus(trendingSelection);
            });
  }

  public void updateSelection(SelectionStatus selectionStatus, String selectionChannel) {
    getTrendingEvents(selectionChannel)
        .forEach(
            (TrendingEvent trendingSelection) -> {
              OutputOutcome outcome = trendingSelection.getMarkets().get(0).getOutcomes().get(0);
              Optional.ofNullable(selectionStatus.getStatus())
                  .ifPresent(status -> outcome.setOutcomeStatusCode(status));
              Optional.ofNullable(selectionStatus.getDisplayed())
                  .ifPresent(displayed -> outcome.setIsDisplayed("Y".equalsIgnoreCase(displayed)));
              updateSelectionStatusAndOutCome(trendingSelection, selectionStatus);
            });
  }

  // get trending event from popularSelection if not then personlized selection
  private List<TrendingEvent> getTrendingEvents(String channel) {

    return Optional.ofNullable(TrendingBetsContext.getPopularSelections().get(channel))
        .orElse(TrendingBetsContext.getPersonalizedSelections().get(channel));
  }

  private void updateSelectionStatusAndOutCome(
      TrendingEvent trendingEvent, SelectionStatus selectionStatus) {
    if (selectionStatus.getPriceDen() != null && selectionStatus.getPriceNum() != null) {
      OutputPrice price = trendingEvent.getMarkets().get(0).getOutcomes().get(0).getPrices().get(0);
      Integer priceDen = selectionStatus.getPriceDen();
      Integer priceNum = selectionStatus.getPriceNum();
      double priceDec =
          1
              + BigDecimal.valueOf(Double.valueOf(priceNum) / priceDen)
                  .setScale(SCALE_VALUE, RoundingMode.HALF_UP)
                  .doubleValue();
      price.setPriceDen(priceDen);
      price.setPriceNum(priceNum);
      price.setPriceDec(priceDec);
    }
    updateSuspendStatus(trendingEvent);
  }

  private void updateSuspendStatus(TrendingEvent trendingEvent) {
    String eventStatusCode = trendingEvent.getEventStatusCode();
    String marketStatusCode = trendingEvent.getMarkets().get(0).getMarketStatusCode();
    String outcomeStatusCode =
        trendingEvent.getMarkets().get(0).getOutcomes().get(0).getOutcomeStatusCode();
    trendingEvent.setIsSuspended(
        !(isActive(eventStatusCode) && isActive(marketStatusCode) && isActive(outcomeStatusCode)));
  }

  private boolean isActive(String status) {
    return "A".equals(status);
  }
}
