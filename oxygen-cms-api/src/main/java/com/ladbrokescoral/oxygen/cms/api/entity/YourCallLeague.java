package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "ycleagues")
@Data
@EqualsAndHashCode(callSuper = true)
public class YourCallLeague extends SortableEntity implements HasBrand {
  @NotBlank private String name;
  private String lang = "en";
  @NotBlank private String brand;
  private boolean enabled = true;
  private boolean activeFor5aSide = false;
  @NotNull private Integer typeId;
}
