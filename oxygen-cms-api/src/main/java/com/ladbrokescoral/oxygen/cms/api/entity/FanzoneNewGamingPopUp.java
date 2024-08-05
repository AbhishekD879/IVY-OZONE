package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzoneNewGamingPopUp")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
public class FanzoneNewGamingPopUp extends AbstractTimelineEntity<FanzoneNewGamingPopUp>
    implements HasBrand {
  @NotNull private String brand;
  private String title;
  private String description;
  private String closeCTA;
  private String playCTA;
  private String updatedByUserName;
  private String createdByUserName;
}
