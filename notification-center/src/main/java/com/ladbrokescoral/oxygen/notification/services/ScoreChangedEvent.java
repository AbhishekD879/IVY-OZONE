package com.ladbrokescoral.oxygen.notification.services;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;
import org.springframework.context.ApplicationEvent;

@EqualsAndHashCode
@ToString
public class ScoreChangedEvent extends ApplicationEvent {

  @Getter private final ScoresDto scores;

  public ScoreChangedEvent(Object source, ScoresDto scores) {
    super(source);
    this.scores = scores;
  }
}
