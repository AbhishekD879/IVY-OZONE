package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;

public class OrderedOutcomeMarketMapper extends ChainedMarketMapper {

  private OrderedOutcomeMarketHelper orderedOutcomeMarketHelper;

  public OrderedOutcomeMarketMapper(
      MarketMapper chain, OrderedOutcomeMarketHelper orderedOutcomeMarketHelper) {
    super(chain);
    this.orderedOutcomeMarketHelper = orderedOutcomeMarketHelper;
  }

  @Override
  public void populate(OutputMarket outputMarket, Event event, Market market) {

    if ("FOOTBALL".equals(event.getCategoryCode())
        && ("Extra-Time Result".equals(outputMarket.getName())
            || outputMarket.getName().toLowerCase().contains("Team to Score".toLowerCase()))) {
      orderedOutcomeMarketHelper.recalculateCorrectedMeaningMinorCode(event, outputMarket);
    }
  }
}
