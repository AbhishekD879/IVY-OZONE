package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzoneclub")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
public class FanzoneClub extends FanzonePage {
  private Boolean active;
  @NotNull private Instant validityPeriodStart;
  @NotNull private Instant validityPeriodEnd;
  private String title;
  private String bannerLink;
  private String description;
  private String updatedByUserName;
  private String createdByUserName;
}
