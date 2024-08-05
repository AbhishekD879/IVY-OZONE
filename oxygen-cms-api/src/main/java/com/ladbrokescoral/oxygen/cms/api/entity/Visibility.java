package com.ladbrokescoral.oxygen.cms.api.entity;

import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class Visibility {

  private boolean enabled = false;
  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;
}
