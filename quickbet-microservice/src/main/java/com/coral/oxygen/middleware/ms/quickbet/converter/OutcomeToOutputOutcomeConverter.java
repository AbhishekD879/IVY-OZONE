package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Outcome;
import org.springframework.stereotype.Component;

@Component
public class OutcomeToOutputOutcomeConverter extends BaseConverter<Outcome, OutputOutcome> {

  @Override
  protected OutputOutcome populateResult(Outcome outcome, OutputOutcome outputOutcome) {
    outputOutcome.setId(outcome.getId());
    outputOutcome.setName(outcome.getName());
    outputOutcome.setOutcomeStatusCode(outcome.getOutcomeStatusCode());
    outputOutcome.setOutcomeMeaningMajorCode(outcome.getOutcomeMeaningMajorCode());
    outputOutcome.setOutcomeMeaningMinorCode(outcome.getOutcomeMeaningMinorCode());
    outputOutcome.setHasPriceStream(outcome.isHasPriceStream());
    return outputOutcome;
  }

  @Override
  protected OutputOutcome createTarget() {
    return new OutputOutcome();
  }
}
