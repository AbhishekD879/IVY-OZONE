package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;

public interface MarketMapper {

  OutputMarket map(Event event, Market market);
}
