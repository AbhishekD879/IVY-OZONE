package com.coral.oxygen.middleware.common.mappers;

import static com.coral.oxygen.middleware.pojos.model.output.utils.ModelMarketUtils.getMarketsColumnsNumberForExceptions;
import static com.coral.oxygen.middleware.pojos.model.output.utils.ModelMarketUtils.marketColumnNumber;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;

public class MarketViewTypeMapper extends ChainedMarketMapper {

  public MarketViewTypeMapper(MarketMapper chain) {
    super(chain);
  }

  @Override
  public void populate(OutputMarket result, Event event, Market market) {
    result.setViewType(calculateViewType(market, event));
  }

  private String calculateViewType(Market market, Event parentEvent) {
    // currently handicaps redesign is not supported only for all sports
    if ("MH".equals(market.getMarketMeaningMinorCode())
        && "FOOTBALL".equals(parentEvent.getCategoryCode())) {
      return "handicaps";
    }
    if ("CS".equals(market.getMarketMeaningMinorCode())
        && "FOOTBALL".equals(parentEvent.getCategoryCode())) {
      return "correctScore";
    }
    String marketColumnsCount =
        market.getDispSortName() != null && !market.getDispSortName().equals("")
            ? marketColumnNumber(market.getDispSortName())
            : getMarketsColumnsNumberForExceptions(market.getOutcomes().size());

    // in case of less amount of outcomes, display them in correct column
    if (marketColumnsCount.compareTo(String.valueOf(market.getOutcomes().size())) > 0
        && !marketColumnsCount.equals("1")
        && market.getOutcomes().size() > 1) {
      marketColumnsCount = "2-3";
    }
    return "columns-" + marketColumnsCount;
  }
}
