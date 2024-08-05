package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class FanzoneNewSignpostingDto extends AbstractTimelineEntity<FanzoneNewSignpostingDto> {
  @NotNull private String brand;
  private Boolean active;
  private String newSignPostingIcon;
  @NotNull private Instant startDate;
  @NotNull private Instant endDate;
  private String updatedByUserName;
  private String createdByUserName;
}
