package com.egalacoral.spark.timeform.model;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Type;

public class LostOutcome extends LostEvent {

  private final Market market;
  private final Outcome outcome;

  public LostOutcome(Type type, Event event, Market market, Outcome outcome) {
    super(type, event);
    this.market = market;
    this.outcome = outcome;
  }

  public Outcome getOutcome() {
    return outcome;
  }

  public Market getMarket() {
    return market;
  }
}
