package com.coral.oxygen.middleware.util;

import com.coral.oxygen.middleware.in_play.service.model.safbaf.KafkaSafUpdate;
import org.junit.Assert;
import org.junit.Test;

public class JsonUtilTest {

  @Test
  public void JsonUtilToJsonAndFromJsonTest() {
    String toJsonFromString = "JsonUtil";
    String eventDataNull =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":null}}";

    String toJson = JsonUtil.toJson(toJsonFromString);
    KafkaSafUpdate fromJson = JsonUtil.fromJson(eventDataNull, KafkaSafUpdate.class);
    Assert.assertNotNull(toJson);
    Assert.assertNotNull(fromJson);
  }
}
