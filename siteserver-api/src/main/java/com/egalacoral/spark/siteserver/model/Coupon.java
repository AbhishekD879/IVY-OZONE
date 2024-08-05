package com.egalacoral.spark.siteserver.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Coupon extends Identity {
  private String id;
  private String classId;
  private String name;
  private String couponSortCode;
  private Integer displayOrder;
  private String siteChannels;
  private String className;
  private Integer classDisplayOrder;
  private String classSortCode;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private Integer categoryDisplayOrder;
}
