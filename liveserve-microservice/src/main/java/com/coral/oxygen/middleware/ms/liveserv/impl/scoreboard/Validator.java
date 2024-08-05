package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Objects;

public abstract class Validator {

  private final Validator next;

  public Validator(Validator next) {
    this.next = next;
  }

  protected abstract boolean checkCondition(ScoreboardEvent event);

  public boolean validate(ScoreboardEvent event) {
    if (!checkCondition(event)) {
      return false;
    }
    if (Objects.isNull(next)) {
      return true;
    }

    return next.validate(event);
  }
}
