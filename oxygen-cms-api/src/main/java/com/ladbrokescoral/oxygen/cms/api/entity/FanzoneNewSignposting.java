package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzoneNewSignposting")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
public class FanzoneNewSignposting extends AbstractTimelineEntity<FanzoneNewSignposting>
    implements HasBrand {
  @NotNull private String brand;
  private Boolean active;
  private String newSignPostingIcon;
  @NotNull private Instant startDate;
  @NotNull private Instant endDate;
  private String updatedByUserName;
  private String createdByUserName;
}
