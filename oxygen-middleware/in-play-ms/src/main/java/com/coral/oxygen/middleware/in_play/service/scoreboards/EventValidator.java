package com.coral.oxygen.middleware.in_play.service.scoreboards;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class EventValidator {

  private final FootballValidator footballValidator;

  public boolean validate(ScoreboardEvent scoreboardEvent) {
    boolean isValid = false;

    switch (scoreboardEvent.getSportCategory()) {
      case "football":
        isValid = this.footballValidator.validate(scoreboardEvent);
        break;
        // placeholder for other sports. currently validating only football events
      default:
        log.debug("{} is not supported", scoreboardEvent.getSportCategory());
        break;
    }
    return isValid;
  }
}
