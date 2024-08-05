package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputMarket;
import com.egalacoral.spark.siteserver.model.Market;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class MarketToOutputMarketConverter extends BaseConverter<Market, OutputMarket> {

  private OutcomeToOutputOutcomeConverter outcomeToOutputOutcomeConverter;

  @Autowired
  public MarketToOutputMarketConverter(
      OutcomeToOutputOutcomeConverter outcomeToOutputOutcomeConverter) {
    this.outcomeToOutputOutcomeConverter = outcomeToOutputOutcomeConverter;
  }

  @Override
  protected OutputMarket populateResult(Market market, OutputMarket outputMarket) {
    outputMarket.setId(market.getId());
    outputMarket.setName(market.getName());
    outputMarket.setMarketStatusCode(market.getMarketStatusCode());
    if (market.getOutcomes() != null) {
      outputMarket.setOutcomes(outcomeToOutputOutcomeConverter.convert(market.getOutcomes()));
    }
    outputMarket.setIsLpAvailable(market.getIsLpAvailable());
    outputMarket.setIsSpAvailable((market.getIsSpAvailable()));
    outputMarket.setIsGpAvailable((market.getIsGpAvailable()));
    outputMarket.setIsEachWayAvailable(market.getIsEachWayAvailable());
    outputMarket.setEachWayFactorDen(market.getEachWayFactorDen());
    outputMarket.setEachWayFactorNum(market.getEachWayFactorNum());
    outputMarket.setIsMarketBetInRun(market.getIsMarketBetInRun());
    outputMarket.setDrilldownTagNames(market.getDrilldownTagNames());
    outputMarket.setIsCashoutAvailable(market.getCashoutAvail());
    outputMarket.setFlags(market.getFlags());
    return outputMarket;
  }

  @Override
  protected OutputMarket createTarget() {
    return new OutputMarket();
  }
}
