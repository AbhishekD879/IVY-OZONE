package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import com.entain.oxygen.promosandbox.utils.SparkTestConfig;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
class HouseKeepingServiceTest {

  @InjectMocks private HouseKeepingService houseKeepingService;

  @Test
  void dropSparkTempTableSuccessTest() {
    ReflectionTestUtils.setField(
        houseKeepingService, IConstantsTest.SPARK_SESSION, SparkTestConfig.getSparkSession());
    assertTrue(
        houseKeepingService.dropSparkTempTable(
            IConstantsTest.PROMOTION_ID, IConstantsTest.LEADERBOARD_ID));
  }

  @Test
  void dropSparkTempTableFailedTest() {
    ReflectionTestUtils.setField(houseKeepingService, IConstantsTest.SPARK_SESSION, null);
    assertFalse(
        houseKeepingService.dropSparkTempTable(
            IConstantsTest.PROMOTION_ID, IConstantsTest.LEADERBOARD_ID));
  }
}
