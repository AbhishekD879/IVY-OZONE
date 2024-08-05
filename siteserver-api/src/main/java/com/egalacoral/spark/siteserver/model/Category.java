package com.egalacoral.spark.siteserver.model;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * This class represents {@code class} SiteServer's entity, NOT actual {@code category}.
 *
 * <p>FIXME: Needs to be renamed into Class in the future.
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class Category extends IdentityWithChildren {

  private Integer id;
  private String name;
  private String classStatusCode;
  private Boolean isActive;
  private Integer displayOrder;
  private String siteChannels;
  private String classFlagCodes;
  private String classSortCode;
  private Integer categoryId;
  private String categoryCode;
  private String categoryName;
  private Integer categoryDisplayOrder;
  private Boolean hasOpenEvent;
  private Boolean hasNext24HourEvent;

  public List<Type> getTypes() {
    return getConcreteChildren(Children::getType);
  }
}
