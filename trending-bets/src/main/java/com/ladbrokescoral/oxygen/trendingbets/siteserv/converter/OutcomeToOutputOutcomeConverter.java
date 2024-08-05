package com.ladbrokescoral.oxygen.trendingbets.siteserv.converter;

import com.egalacoral.spark.siteserver.model.Outcome;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputOutcome;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class OutcomeToOutputOutcomeConverter extends BaseConverter<Outcome, OutputOutcome> {

  private PriceToOutputPriceConverter priceToOutputPriceConverter;

  @Autowired
  public OutcomeToOutputOutcomeConverter(PriceToOutputPriceConverter priceToOutputPriceConverter) {
    this.priceToOutputPriceConverter = priceToOutputPriceConverter;
  }

  @Override
  protected OutputOutcome populateResult(Outcome outcome, OutputOutcome outputOutcome) {
    outputOutcome.setId(outcome.getId());
    outputOutcome.setName(outcome.getName());
    outputOutcome.setLiveServChannels(
        outcome.getLiveServChannels().contains(",")
            ? outcome.getLiveServChannels().split(",")[0]
            : outcome.getLiveServChannels());
    outputOutcome.setOutcomeStatusCode(outcome.getOutcomeStatusCode());
    outputOutcome.setOutcomeMeaningMajorCode(outcome.getOutcomeMeaningMajorCode());
    outputOutcome.setPrices(priceToOutputPriceConverter.convert(outcome.getPrices()));
    outputOutcome.setMarketId(outcome.getMarketId());
    outputOutcome.setIsActive(outcome.getIsActive());
    outputOutcome.setIsDisplayed(outcome.getIsDisplayed());
    outputOutcome.setDrilldownTagNames(outcome.getDrilldownTagNames());
    outputOutcome.setLiveServChildrenChannels(outcome.getLiveServChildrenChannels());
    return outputOutcome;
  }

  @Override
  protected OutputOutcome createTarget() {
    return new OutputOutcome();
  }
}
