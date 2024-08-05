package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
@EqualsAndHashCode(callSuper = true)
public class AbstractMenuEntity extends SortableEntity {

  @com.ladbrokescoral.oxygen.cms.api.service.validators.Brand private String brand;

  @NotNull @NotBlank private String linkTitle;

  @Field("linkTitle_brand")
  private String linkTitleBrand;
}
