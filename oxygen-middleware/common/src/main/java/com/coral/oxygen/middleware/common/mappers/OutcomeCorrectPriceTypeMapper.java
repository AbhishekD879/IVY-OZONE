package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;

public class OutcomeCorrectPriceTypeMapper extends ChainedOutcomeMapper {

  public OutcomeCorrectPriceTypeMapper(OutcomeMapper outcomeMapper) {
    super(outcomeMapper);
  }

  @Override
  protected void populate(OutputOutcome result, Event event, Market market, Outcome outcome) {
    result.setCorrectPriceType(calculateCorrectPriceType(market, outcome));
  }

  private boolean isTrue(Boolean b) {
    return Boolean.TRUE.equals(b);
  }

  /* modified the existing condition to cover sonar as the earlier was unreachable */
  private String calculateCorrectPriceType(Market parentMarket, Outcome outcome) {
    if (isTrue(parentMarket.getIsSpAvailable())) {
      if (!isTrue(parentMarket.getIsLpAvailable()) || outcome.getPrices() == null) {
        return "SP";
      }
    }

    if ((isTrue(parentMarket.getIsLpAvailable())) && (outcome.getPrices() != null)) {
      return "LP";
    }
    return null;
  }
}
