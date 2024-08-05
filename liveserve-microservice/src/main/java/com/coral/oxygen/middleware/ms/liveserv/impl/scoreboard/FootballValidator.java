package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import org.springframework.stereotype.Service;

@Service
public class FootballValidator {

  private Validator validator;

  public FootballValidator() {
    ProviderValidator providerValidator = new ProviderValidator(null);
    this.validator = new PeriodValidator(providerValidator);
  }

  public boolean validate(ScoreboardEvent scoreboardEvent) {
    return validator.validate(scoreboardEvent);
  }
}
