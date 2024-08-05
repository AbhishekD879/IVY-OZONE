package com.egalacoral.spark.siteserver.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

/** This class represents {@code category} SiteServer's entity */
@Data
@EqualsAndHashCode(callSuper = true)
public class CategoryEntity extends IdentityWithChildren {

  private Integer id;
  private String name;
  private String categoryCode;
  private Boolean isDisplayed;
  private Integer displayOrder;
}
