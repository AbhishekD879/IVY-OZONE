package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
public class FanzoneClubDto extends FanzonePageDto {
  private Boolean active;
  @NotNull private Instant validityPeriodStart;
  @NotNull private Instant validityPeriodEnd;
  private String title;
  private String bannerLink;
  private String description;
  private String updatedByUserName;
  private String createdByUserName;
}
