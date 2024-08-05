package com.coral.oxygen.middleware.pojos.model.output;

import java.io.Serializable;
import java.time.Instant;
import lombok.Data;

@Data
public class NextRacesClfDto implements Serializable {
  private Instant lastEventTime;
  private boolean enabled;
}
