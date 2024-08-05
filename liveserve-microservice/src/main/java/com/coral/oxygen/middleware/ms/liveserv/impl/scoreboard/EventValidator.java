package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class EventValidator {

  private final FootballValidator footballValidator;

  public boolean validate(ScoreboardEvent event) {
    switch (event.getSportCategory()) {
      case "football":
        return footballValidator.validate(event);
      default:
        log.debug("{} is not supported", event.getSportCategory());
    }
    return false;
  }
}
