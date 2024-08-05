package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import javax.json.JsonString;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class PeriodValidator extends Validator {

  private List<String> NOT_SUPPORTED_PERIODS =
      Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen");

  public PeriodValidator(Validator next) {
    super(next);
  }

  @Override
  protected boolean checkCondition(ScoreboardEvent event) {
    JsonString period = event.getEventStructure().getJsonString("period");
    boolean periodIsNotPreMatch =
        Objects.nonNull(period) && !hasNotSupportedPeriod(period.getString());
    if (!periodIsNotPreMatch) {
      log.debug(
          "Scoreboard update {} for event {} currently is not live-match",
          event.getSequenceId(),
          event.getObEventId());
    }
    return periodIsNotPreMatch;
  }

  private boolean hasNotSupportedPeriod(String period) {
    return NOT_SUPPORTED_PERIODS.stream().anyMatch(period::equalsIgnoreCase);
  }
}
