package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "navigationgroup")
public class NavigationGroup extends AbstractEntity implements HasBrand {
  @NotBlank private String brand;
  @NotBlank private String title;
  private Boolean status;
}
