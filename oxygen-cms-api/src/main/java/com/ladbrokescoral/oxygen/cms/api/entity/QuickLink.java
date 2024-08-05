package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "quicklinks")
@Data
@EqualsAndHashCode(callSuper = true)
public class QuickLink extends SortableEntity implements HasBrand {
  private Instant validityPeriodEnd;
  private Instant validityPeriodStart;
  private String target;
  private String body;
  private String title;
  private Boolean disabled;
  private String lang;
  @NotBlank private String brand;
  private String linkType;
  private String raceType;
  private Filename filename;
  private Integer heightMedium;
  private String uriMedium;
  private Integer widthMedium;
  private String uriLarge;
}
