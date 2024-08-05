package com.coral.siteserver.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Category extends Identity implements Serializable {

  private static final long serialVersionUID = -5858160714213406365L;

  protected List<Children> children;
  protected Integer id;
  protected String name;
  protected String classStatusCode;
  protected Boolean isActive;
  protected Integer displayOrder;
  protected String siteChannels;
  protected String classFlagCodes;
  protected String classSortCode;
  protected Integer categoryId;
  protected String categoryCode;
  protected String categoryName;
  protected Integer categoryDisplayOrder;
  protected Boolean hasOpenEvent;
  protected Boolean hasNext24HourEvent;

  private List<Children> getChildren() {
    if (children == null) return new ArrayList<>();
    return children;
  }

  public List<Type> getTypes() {
    return this.getChildren().stream()
        .map(Children::getType)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  public Integer getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public String getClassStatusCode() {
    return classStatusCode;
  }

  public Boolean getActive() {
    return isActive;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public String getSiteChannels() {
    return siteChannels;
  }

  public String getClassFlagCodes() {
    return classFlagCodes;
  }

  public String getClassSortCode() {
    return classSortCode;
  }

  public Integer getCategoryId() {
    return categoryId;
  }

  public String getCategoryCode() {
    return categoryCode;
  }

  public String getCategoryName() {
    return categoryName;
  }

  public Integer getCategoryDisplayOrder() {
    return categoryDisplayOrder;
  }

  public Boolean getHasOpenEvent() {
    return hasOpenEvent;
  }

  public Boolean getHasNext24HourEvent() {
    return hasNext24HourEvent;
  }

  @Override
  public String toString() {
    return super.toString()
        + ", id="
        + id
        + ", name='"
        + name
        + '\''
        + ", classStatusCode='"
        + classStatusCode
        + '\''
        + ", isActive="
        + isActive
        + ", displayOrder="
        + displayOrder
        + ", siteChannels='"
        + siteChannels
        + '\''
        + ", classFlagCodes='"
        + classFlagCodes
        + '\''
        + ", classSortCode='"
        + classSortCode
        + '\''
        + ", categoryId="
        + categoryId
        + ", categoryCode='"
        + categoryCode
        + '\''
        + ", categoryName='"
        + categoryName
        + '\''
        + ", categoryDisplayOrder='"
        + categoryDisplayOrder
        + '\''
        + ", hasOpenEvent="
        + hasOpenEvent
        + ", hasNext24HourEvent="
        + hasNext24HourEvent
        + ", children="
        + children
        + "} ";
  }
}
