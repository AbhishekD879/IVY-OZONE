package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzoneComingBack")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class FanzoneComingBack extends AbstractTimelineEntity<FanzoneComingBack>
    implements HasBrand {
  @NotNull private String brand;
  private String fzComingBackHeading;
  private String fzComingBackTitle;
  private String fzComingBackDescription;
  private String fzComingBackOKCTA;
  private String fzComingBackDisplayFromDays;
  private String fzComingBackBgImageDesktop;
  private String fzComingBackBgImageMobile;
  private String fzComingBackBadgeUrlDesktop;
  private String fzComingBackBadgeUrlMobile;
  private Boolean fzComingBackPopupDisplay;
  private Instant fzSeasonStartDate;
  private String updatedByUserName;
  private String createdByUserName;
}
