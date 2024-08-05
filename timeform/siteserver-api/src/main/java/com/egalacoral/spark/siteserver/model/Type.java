package com.egalacoral.spark.siteserver.model;

import java.util.List;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Type extends Identity {
  protected List<Children> children;
  protected Integer id;
  protected String name;
  protected String typeStatusCode;
  protected Boolean isActive;
  protected Integer displayOrder;
  protected String siteChannels;
  protected Integer classId;
  protected String cashoutAvail;

  public Integer getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public String getTypeStatusCode() {
    return typeStatusCode;
  }

  public Boolean isActive() {
    return isActive;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public String getSiteChannels() {
    return siteChannels;
  }

  public Integer getClassId() {
    return classId;
  }

  public String getCashoutAvail() {
    return cashoutAvail;
  }

  @Override
  public String toString() {
    return super.toString()
        + ", id="
        + id
        + ", name='"
        + name
        + '\''
        + ", typeStatusCode='"
        + typeStatusCode
        + '\''
        + ", isActive="
        + isActive
        + ", displayOrder="
        + displayOrder
        + ", siteChannels='"
        + siteChannels
        + '\''
        + ", classId="
        + classId
        + ", cashoutAvail='"
        + cashoutAvail
        + '\''
        + ", children="
        + children
        + "} ";
  }
}
