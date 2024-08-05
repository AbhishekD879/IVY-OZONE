package com.ladbrokescoral.oxygen.cms.api.entity;

import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class EventsSelectionSetting {

  @NotNull private Instant from;
  @NotNull private Instant to;
  private boolean autoRefresh;
}
