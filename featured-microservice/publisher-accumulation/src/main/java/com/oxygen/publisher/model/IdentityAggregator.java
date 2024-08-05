package com.oxygen.publisher.model;

import java.math.BigInteger;

/** The aggregation of identities. */
public interface IdentityAggregator {

  String getId();

  default <T extends IdentityAggregator> boolean isEqualsById(T other) {
    return isEqualsById(other.getId());
  }

  default boolean isEqualsById(Integer intId) {
    return isEqualsById(String.valueOf(intId));
  }

  default boolean isEqualsById(String strId) {
    return strId.equals(getId());
  }

  default boolean isEqualsById(BigInteger intId) {
    return isEqualsById(String.valueOf(intId));
  }
}
