package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzoneNewSeason")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class FanzoneNewSeason extends AbstractTimelineEntity<FanzoneNewSeason> implements HasBrand {
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
