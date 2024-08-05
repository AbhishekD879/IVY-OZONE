package com.entain.oxygen.betbuilder_middleware.service;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.entain.oxygen.betbuilder_middleware.api.response.PriceResponse;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;

class BBUtilTest {

  @Mock public BBUtil bbUtil;

  @Test
  void testToJson() {
    PriceResponse obj = new PriceResponse();
    obj.setBatchId("123");
    String json = bbUtil.toJson(obj);

    assertEquals("{\"batchId\":\"123\"}", json);
  }

  @Test
  void testToJsonNull() {
    PriceResponse obj = null;

    String json = bbUtil.toJson(obj);

    assertEquals("", json);
  }
}
