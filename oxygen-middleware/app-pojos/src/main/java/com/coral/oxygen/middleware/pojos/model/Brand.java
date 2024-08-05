package com.coral.oxygen.middleware.pojos.model;

import java.util.stream.Collectors;
import java.util.stream.Stream;

public enum Brand {
  CORAL("bma"),
  LADBROKES("ladbrokes"),
  VANILLA("vanilla");

  private String name;

  Brand(String name) {
    this.name = name;
  }

  public static Brand from(String brand) {
    String validBrands = Stream.of(values()).map(p -> p.name).collect(Collectors.joining(","));
    return Stream.of(values())
        .filter(p -> p.name.equalsIgnoreCase(brand))
        .findAny()
        .orElseThrow(
            () ->
                new IllegalArgumentException(
                    "Provide one brand from list : " + validBrands + " instead of :" + brand));
  }
}
