package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class FanzoneNewGamingPopUpDto extends AbstractTimelineEntity<FanzoneNewGamingPopUpDto> {
  @NotNull private String brand;
  private String title;
  private String description;
  private String closeCTA;
  private String playCTA;
  private String updatedByUserName;
  private String createdByUserName;
}
