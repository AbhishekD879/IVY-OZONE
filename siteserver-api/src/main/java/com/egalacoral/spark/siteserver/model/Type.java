package com.egalacoral.spark.siteserver.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Type extends IdentityWithChildren {

  private Integer id;
  private String name;
  private String typeStatusCode;
  private Boolean isActive;
  private Integer displayOrder;
  private String siteChannels;
  private Integer classId;
  private String cashoutAvail;
}
