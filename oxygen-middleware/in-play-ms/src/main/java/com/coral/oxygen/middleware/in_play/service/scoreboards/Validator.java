package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.util.Objects;

public abstract class Validator {

  private final Validator next;

  protected Validator(Validator next) {
    this.next = next;
  }

  public abstract boolean checkCondition(ScoreboardEvent scoreboardEvent);

  public boolean validate(ScoreboardEvent scoreboardEvent) {
    if (!checkCondition(scoreboardEvent)) {
      return false;
    }
    if (Objects.isNull(next)) {
      return true;
    }
    return next.validate(scoreboardEvent);
  }
}
