package com.coral.oxygen.edp.model.mapping;

import static com.coral.oxygen.edp.model.mapping.config.ModelMarketUtils.getMarketsColumnsNumberForExceptions;
import static com.coral.oxygen.edp.model.mapping.config.ModelMarketUtils.marketColumnNumber;

import com.coral.oxygen.edp.model.output.OutputMarket;
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

    if (marketColumnsCount == null) return null;

    // in case of less amount of outcomes, display them in correct columnS
    if (marketColumnsCount.compareTo(String.valueOf(market.getOutcomes().size())) > 0
        && !marketColumnsCount.equals("1")
        && market.getOutcomes().size() > 1) {
      marketColumnsCount = "2-3";
    }
    return "columns-" + marketColumnsCount;
  }
}
