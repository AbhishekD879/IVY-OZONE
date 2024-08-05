package com.ladbrokescoral.oxygen.cms.api.entity;

import java.time.Instant;
import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class GameEvent {

  private String tvIcon;

  @NotEmpty private String eventId;

  @NotNull private Instant startTime;

  @Valid @NotNull private Team home;

  @Valid @NotNull private Team away;
}
