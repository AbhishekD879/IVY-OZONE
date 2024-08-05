package com.ladbrokescoral.oxygen.cms.api.entity;

import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class BannerEntity extends SortableEntity {
  @NotBlank private String name;
  @NotNull private Instant validityPeriodStart;
  @NotNull private Instant validityPeriodEnd;
  private Boolean disabled;
  protected String brand = "bma";
  private String description;
  private Filename filename;
  private String uriMedium;
  private String uriOriginal;
}
