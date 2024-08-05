package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2;

import static org.assertj.core.api.Assertions.assertThatCode;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class RegularSelectionRequestTest {
  private RegularSelectionRequest request;

  @BeforeEach
  void setUp() {
    request = new RegularSelectionRequest();
  }

  @Test
  void toStringTest() {
    assertThatCode(() -> request.toString()).doesNotThrowAnyException();
  }
}
