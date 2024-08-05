package com.coral.oxygen.middleware.in_play.service.model.safbaf;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.extern.slf4j.Slf4j;

@Data
@EqualsAndHashCode(callSuper = true)
@Slf4j
public class Event extends Entity {
  private Integer eventKey;
  private String eventStatus;
  private String isEventStarted;
  private String parents;
}
