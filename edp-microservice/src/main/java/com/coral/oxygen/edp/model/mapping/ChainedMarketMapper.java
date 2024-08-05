package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public abstract class ChainedMarketMapper implements MarketMapper {

  private final MarketMapper chain;

  public ChainedMarketMapper(MarketMapper chain) {
    this.chain = chain;
  }

  @Override
  public OutputMarket map(Event event, Market market) {
    OutputMarket result = chain.map(event, market);
    populate(result, event, market);
    return result;
  }

  public abstract void populate(OutputMarket result, Event event, Market market);
}
