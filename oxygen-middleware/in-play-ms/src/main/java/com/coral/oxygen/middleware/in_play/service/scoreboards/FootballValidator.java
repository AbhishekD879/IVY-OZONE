package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class FootballValidator {

  private final Validator validator;

  public FootballValidator(
      @Value("${df.periods}") List<String> notSupportedPeriods,
      @Value("${df.providers}") List<String> supportedProviders) {
    ProviderValidator providerValidator = new ProviderValidator(null, supportedProviders);
    this.validator = new PeriodValidator(providerValidator, notSupportedPeriods);
  }

  public boolean validate(ScoreboardEvent scoreboardEvent) {
    return this.validator.validate(scoreboardEvent);
  }
}
