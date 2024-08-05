package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "maintenancepages")
@Data
@EqualsAndHashCode(callSuper = true)
public class MaintenancePage extends SortableEntity implements HasBrand {
  @NotBlank private String name;
  @NotNull private Instant validityPeriodEnd;
  @NotNull private Instant validityPeriodStart;
  private Boolean desktop;
  private Boolean tablet;
  private Boolean mobile;
  private String targetUri;
  @NotBlank private String brand;
  private Filename filename;
  private String uriMedium;
  private String uriOriginal;
}
