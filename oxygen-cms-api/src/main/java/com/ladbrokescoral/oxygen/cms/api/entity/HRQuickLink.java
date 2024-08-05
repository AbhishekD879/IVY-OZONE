package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.MediumImageAbstractMenu;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "hr quicklinks")
@Data
@EqualsAndHashCode(callSuper = true)
public class HRQuickLink extends SortableEntity implements MediumImageAbstractMenu {
  private String body;
  @NotBlank private String brand;
  private Boolean disabled;
  private Filename filename;
  private Integer heightMedium;
  private String lang;
  private String linkType;
  private String raceType;
  @NotBlank private String target;
  private String title;
  private String uriMedium;
  @NotNull private Instant validityPeriodEnd;
  @NotNull private Instant validityPeriodStart;
  private Integer widthMedium;
}
