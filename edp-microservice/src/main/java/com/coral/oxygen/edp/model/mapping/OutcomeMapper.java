package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;

public interface OutcomeMapper {

  OutputOutcome map(Event event, Market market, Outcome outcome);
}
