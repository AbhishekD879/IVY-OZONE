package com.coral.oxygen.middleware.pojos.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.Test;

public class BrandTest {

  @Test
  public void from() {
    assertEquals(Brand.CORAL, Brand.from("bma"));
  }

  @Test(expected = IllegalArgumentException.class)
  public void fromInvalid() {
    Brand.from("bma1");
  }
}
