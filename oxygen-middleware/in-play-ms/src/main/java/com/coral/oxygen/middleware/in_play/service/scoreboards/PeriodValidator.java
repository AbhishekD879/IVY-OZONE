package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.util.List;
import java.util.Objects;
import javax.json.JsonString;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class PeriodValidator extends Validator {

  private final List<String> NOT_SUPPORTED_PERIODS;

  public PeriodValidator(Validator next, List<String> notSupportedPeriods) {
    super(next);
    this.NOT_SUPPORTED_PERIODS = notSupportedPeriods;
  }

  @Override
  public boolean checkCondition(ScoreboardEvent scoreboardEvent) {
    JsonString period = scoreboardEvent.getEventStructure().getJsonString("period");
    boolean periodIsNotPreMatch =
        Objects.nonNull(period) && !hasNotSupportedPeriod(period.getString());
    if (!periodIsNotPreMatch) {
      log.debug(
          "Scoreboard update {} for event {} currently is not live-match",
          scoreboardEvent.getSequenceId(),
          scoreboardEvent.getObEventId());
    }
    return periodIsNotPreMatch;
  }

  private boolean hasNotSupportedPeriod(String period) {
    log.info("PeriodValidator::period is ::{}", period);
    return NOT_SUPPORTED_PERIODS.stream().anyMatch(period::equalsIgnoreCase);
  }
}
