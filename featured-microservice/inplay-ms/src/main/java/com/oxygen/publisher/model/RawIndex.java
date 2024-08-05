package com.oxygen.publisher.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;
import org.apache.commons.lang3.StringUtils;

/**
 * categoryId::topLevelType[::marketSelector][::typeId]
 *
 * <p>Created by Aliaksei Yarotski on 12/8/17.
 */
@Getter
@AllArgsConstructor
@Builder
@ToString
public class RawIndex implements Cloneable, Comparable<RawIndex> {
  private Integer categoryId;
  private String topLevelType;
  private String marketSelector;
  private Integer typeId;

  public RawIndex(SportSegment sportSegment) {
    this.categoryId = sportSegment.getCategoryId();
    this.topLevelType = sportSegment.getTopLevelType();
    this.marketSelector = sportSegment.getMarketSelector();
  }

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
        this.typeId = Integer.parseInt(keys[2]);
      } else {
        this.marketSelector = keys[2];
      }
    }
    if (keys.length == 4) {
      this.typeId = Integer.parseInt(keys[3]);
    }
  }

  public String toStructuredKey() {
    StringBuffer result = new StringBuffer();
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

  /**
   * [clone]::[clone]::[null]::[null]
   *
   * @return reference onto entity form the cache.
   */
  public RawIndex cloneToRoot() {
    RawIndex clone = this.clone();
    clone.typeId = null;
    clone.marketSelector = null;
    return clone;
  }

  /**
   * [clone]::[clone]::[new]::[clone]
   *
   * @param market new value of market selector name.
   * @return clone for new market selector name.
   */
  public RawIndex cloneToMarket(String market) {
    RawIndex clone = this.clone();
    clone.marketSelector = market;
    return clone;
  }

  /**
   * [clone]::[clone]::[clone]::[new]
   *
   * @param typeId new value of type ID.
   * @return clone for new type.
   */
  public RawIndex cloneToType(Integer typeId) {
    RawIndex clone = this.clone();
    clone.typeId = typeId;
    return clone;
  }

  /**
   * @return clone as is.
   */
  public RawIndex clone() {
    try {
      return (RawIndex) super.clone();
    } catch (CloneNotSupportedException e) {
      throw new RuntimeException();
    }
  }

  /**
   * Lower when close to root of the hierarchy.
   *
   * @param left this index.
   * @param right other index.
   * @return
   */
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

  public int getLevel() {
    if (this.marketSelector == null && this.typeId == null) {
      return 0;
    } else if (this.marketSelector == null) {
      return 1;
    } else if (this.typeId == null) {
      return 2;
    }
    return 3;
  }
}
