package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;

public class MarketHandicapTypeMapper extends ChainedMarketMapper {

  public MarketHandicapTypeMapper(MarketMapper chain) {
    super(chain);
  }

  @Override
  public void populate(OutputMarket result, Event event, Market market) {
    result.setHandicapType(calculateHandicapType(market, event));
  }

  private String calculateHandicapType(Market market, Event parentEvent) {
    if ("FOOTBALL".equals(parentEvent.getCategoryCode())
        && "MH".equals(market.getMarketMeaningMinorCode())) {
      if (market.getCollectionNames() == null) {
        return null;
      }
      if (market.getCollectionNames().contains("Handicap Match Result")) {
        return "matchResult";
      } else if (market.getCollectionNames().contains("Handicap First Half")) {
        return "firstHalf";
      } else if (market.getCollectionNames().contains("Handicap Second Half")) {
        return "secondHalf";
      }
    }
    return null;
  }
}
