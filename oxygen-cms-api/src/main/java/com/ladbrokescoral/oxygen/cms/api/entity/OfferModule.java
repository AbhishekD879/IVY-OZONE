package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "offermodules")
@Data
@EqualsAndHashCode(callSuper = true)
public class OfferModule extends SortableEntity implements HasBrand {
  @NotBlank private String name;
  @NotBlank private String brand;
  private Boolean disabled;
  private String showModuleOn;
}
