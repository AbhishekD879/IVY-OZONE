package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzoneoptinemail")
public class FanzoneOptinEmail extends AbstractTimelineEntity<FanzoneOptinEmail>
    implements HasBrand {
  @NotNull private String brand;
  private String fanzoneEmailPopupTitle;
  private String fanzoneEmailPopupDescription;
  private String fanzoneEmailPopupOptIn;
  private String fanzoneEmailPopupRemindMeLater;
  private String fanzoneEmailPopupDontShowThisAgain;
  private Instant seasonStartDate;
  private Instant seasonEndDate;
}
