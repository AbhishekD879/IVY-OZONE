package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class BetPackOnboardingDto {

  private String id;
  @NotNull private String brand;
  @NotNull private Boolean isActive;
  private String createdBy;
  private String createdByUserName;
  private String updatedBy;
  private String updatedByUserName;
  private Instant createdAt;
  private Instant updatedAt;

  @Valid private List<OnboardingImageDto> images;
}
