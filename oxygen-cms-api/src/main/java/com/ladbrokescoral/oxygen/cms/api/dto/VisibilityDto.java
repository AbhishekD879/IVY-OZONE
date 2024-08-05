package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.Data;

@Data
public class VisibilityDto {
  private boolean enabled;
  private Instant displayFrom;
  private Instant displayTo;
}
