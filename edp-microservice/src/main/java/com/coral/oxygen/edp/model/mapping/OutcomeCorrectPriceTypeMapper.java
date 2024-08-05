package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputOutcome;
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

  private boolean isLpAvailableFalseOrPricesNull(Market parentMarket, Outcome outcome) {
    return !isTrue(parentMarket.getIsLpAvailable()) || outcome.getPrices() == null;
  }

  /* modified the existing condition to cover sonar as the earlier was unreachable */
  private String calculateCorrectPriceType(Market parentMarket, Outcome outcome) {
    if (isTrue(parentMarket.getIsSpAvailable())
        && isLpAvailableFalseOrPricesNull(parentMarket, outcome)) {
      return "SP";
    }
    if ((isTrue(parentMarket.getIsLpAvailable())) && (outcome.getPrices() != null)) {
      return "LP";
    }
    return null;
  }
}
