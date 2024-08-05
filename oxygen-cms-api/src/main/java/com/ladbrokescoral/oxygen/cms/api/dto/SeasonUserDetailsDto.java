package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class SeasonUserDetailsDto extends SeasonDetailsDto {
  private String createdBy;
  private String createdByUserName;
  private String updatedBy;
  private String updatedByUserName;
  private Instant createdAt;
  private Instant updatedAt;
}
