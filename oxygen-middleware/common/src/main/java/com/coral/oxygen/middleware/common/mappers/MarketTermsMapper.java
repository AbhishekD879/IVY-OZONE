package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.util.StringJoiner;

public class MarketTermsMapper extends ChainedMarketMapper {

  public MarketTermsMapper(MarketMapper chain) {
    super(chain);
  }

  @Override
  public void populate(OutputMarket result, Event event, Market market) {
    result.setTerms(calculateTerms(market));
  }

  private String calculateTerms(Market market) {
    if (market.getEachWayPlaces() != null) {
      return "Each Way: "
          + market.getEachWayFactorNum()
          + "/"
          + market.getEachWayFactorDen()
          + " odds - places "
          + calculateEachWayPlaces(market.getEachWayPlaces());
    }
    return null;
  }

  private String calculateEachWayPlaces(Integer num) {
    StringJoiner eachWP = new StringJoiner(",");
    for (int i = 1; i <= num; i++) {
      eachWP.add(String.valueOf(i));
    }
    return eachWP.toString();
  }
}
