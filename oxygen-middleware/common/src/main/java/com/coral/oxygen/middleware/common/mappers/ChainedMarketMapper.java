package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
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
    try {
      populate(result, event, market);
    } catch (Exception e) {
      log.error(
          "Suppressed error during market mapping in class " + this.getClass().getCanonicalName(),
          e);
    }
    return result;
  }

  public abstract void populate(OutputMarket result, Event event, Market market);
}
