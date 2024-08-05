package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class FanzoneNewSeasonDto extends AbstractTimelineEntity<FanzoneNewSeasonDto> {
  @NotNull private String brand;
  private String fzNewSeasonHeading;
  private String fzNewSeasonTitle;
  private String fzNewSeasonDescription;
  private String fzNewSeasonBgImageDesktop;
  private String fzNewSeasonBgImageMobile;
  private String fzNewSeasonBadgeDesktop;
  private String fzNewSeasonBadgeMobile;
  private String fzNewSeasonLightningDesktop;
  private String fzNewSeasonLightningMobile;
  private String updatedByUserName;
  private String createdByUserName;
}
