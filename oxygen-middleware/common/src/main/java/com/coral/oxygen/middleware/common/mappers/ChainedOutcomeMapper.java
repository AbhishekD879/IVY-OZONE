package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public abstract class ChainedOutcomeMapper implements OutcomeMapper {

  private final OutcomeMapper chain;

  public ChainedOutcomeMapper(OutcomeMapper outcomeMapper) {
    this.chain = outcomeMapper;
  }

  @Override
  public OutputOutcome map(Event event, Market market, Outcome outcome) {
    OutputOutcome result = chain.map(event, market, outcome);
    try {
      populate(result, event, market, outcome);
    } catch (Exception e) {
      log.error(
          "Suppressed error during outcome mapping in class " + this.getClass().getCanonicalName(),
          e);
    }
    return result;
  }

  protected abstract void populate(
      OutputOutcome result, Event event, Market market, Outcome outcome);
}
