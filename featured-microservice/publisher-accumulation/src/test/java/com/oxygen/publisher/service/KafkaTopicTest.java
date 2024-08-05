package com.oxygen.publisher.service;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class KafkaTopicTest {

  @Test
  public void kafkaTopicTest() {
    Assert.assertEquals(
        "VIRTUAL_SPORTS_RIBBON_CHANGED", KafkaTopic.Topic.VIRTUAL_SPORTS_RIBBON_CHANGED.toString());
  }
}
