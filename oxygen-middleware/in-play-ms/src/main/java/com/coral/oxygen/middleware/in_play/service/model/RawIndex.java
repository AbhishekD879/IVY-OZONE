package com.coral.oxygen.middleware.in_play.service.model;

import lombok.NoArgsConstructor;
import org.apache.commons.lang3.StringUtils;

/**
 * categoryId::topLevelType[::marketSelector][::typeId]
 *
 * <p>Created by Aliaksei Yarotski on 12/8/17.
 */
@NoArgsConstructor
public class RawIndex implements Cloneable, Comparable<RawIndex> {
  private Integer categoryId;
  private String topLevelType;
  private String marketSelector;
  private String typeId;

  /**
   * Parse string key by mask categoryId::topLevelType[::marketSelector][::typeId]
   *
   * @param key
   */
  public RawIndex(String key) {
    String[] keys = key.split("::");
    if (keys.length > 0) {
      this.categoryId = Integer.parseInt(keys[0]);
    }
    if (keys.length > 1) {
      this.topLevelType = keys[1];
    }
    if (keys.length > 2) {
      if (StringUtils.isNumeric(keys[2])) {
        this.typeId = keys[2];
      } else {
        this.marketSelector = keys[2];
      }
    }
    if (keys.length == 4) {
      this.typeId = keys[3];
    }
  }

  public Integer getCategoryId() {
    return categoryId;
  }

  public String getTopLevelType() {
    return topLevelType;
  }

  public String getMarketSelector() {
    return marketSelector;
  }

  public String getTypeId() {
    return typeId;
  }

  public RawIndex marketSelector(String marketSelector) {
    this.marketSelector = marketSelector;
    return this;
  }

  public RawIndex topLevelType(String topLevelType) {
    this.topLevelType = topLevelType;
    return this;
  }

  public RawIndex categoryId(Integer categoryId) {
    this.categoryId = categoryId;
    return this;
  }

  public RawIndex typeId(String typeId) {
    this.typeId = typeId;
    return this;
  }

  public String toStructuredKey() {
    StringBuilder result = new StringBuilder();
    result.append(categoryId).append("::").append(topLevelType);
    if (marketSelector != null) {
      result.append("::").append(marketSelector);
    }
    if (typeId != null) {
      result.append("::").append(typeId);
    }
    return result.toString();
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    RawIndex rawIndex = (RawIndex) o;

    if (!categoryId.equals(rawIndex.categoryId)) return false;
    if (!topLevelType.equals(rawIndex.topLevelType)) return false;
    if (marketSelector != null
        ? !marketSelector.equals(rawIndex.marketSelector)
        : rawIndex.marketSelector != null) return false;
    return typeId != null ? typeId.equals(rawIndex.typeId) : rawIndex.typeId == null;
  }

  @Override
  public int hashCode() {
    int result = categoryId.hashCode();
    result = 31 * result + topLevelType.hashCode();
    result = 31 * result + (marketSelector != null ? marketSelector.hashCode() : 0);
    result = 31 * result + (typeId != null ? typeId.hashCode() : 0);
    return result;
  }

  public RawIndex clone() {
    try {
      return (RawIndex) super.clone();
    } catch (CloneNotSupportedException e) {
      throw new RuntimeException();
    }
  }

  public static int compare(RawIndex left, RawIndex right) {
    if (left.getMarketSelector() != null && right.getMarketSelector() == null) {
      return -1;
    }
    if (left.getTypeId() != null && right.getTypeId() == null) {
      return -1;
    }
    if (left.getMarketSelector() == null
        && right.getMarketSelector() == null
        && left.getTypeId() == null
        && right.getTypeId() == null) {
      return 0;
    }
    if (left.getMarketSelector() == null
        && right.getMarketSelector() == null
        && left.getTypeId() != null
        && right.getTypeId() != null) {
      return 0;
    }
    if (left.getTypeId() == null && right.getTypeId() == null) {
      return 0;
    }
    if (left.getMarketSelector() != null
        && right.getMarketSelector() != null
        && left.getTypeId() != null
        && right.getTypeId() != null) {
      return 0;
    }
    return 1;
  }

  @Override
  public int compareTo(RawIndex another) {
    return compare(this, another);
  }
}
