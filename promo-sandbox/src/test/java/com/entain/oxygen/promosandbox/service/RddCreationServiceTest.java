package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import com.entain.oxygen.promosandbox.utils.SparkTestConfig;
import java.util.ArrayList;
import org.apache.spark.sql.types.StructType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
class RddCreationServiceTest {

  @InjectMocks private RddCreationService RDDCreationService;

  @BeforeEach
  void beforeEachSetup() {
    ReflectionTestUtils.setField(
        RDDCreationService, IConstantsTest.SPARK_SESSION, SparkTestConfig.getSparkSession());
  }

  @Test
  void createPromoUserRDDSuccessTest() {
    UserRankInfoDto userRankInfoDto = new UserRankInfoDto();
    userRankInfoDto.setRowList(new ArrayList<>());
    userRankInfoDto.setStructType(new StructType());
    assertTrue(
        RDDCreationService.createPromoUserRDD(
            userRankInfoDto, IConstantsTest.PROMOTION_ID, IConstantsTest.LEADERBOARD_ID));
  }

  @Test
  void createPromoUserRDDFailedTest() {
    assertFalse(
        RDDCreationService.createPromoUserRDD(
            new UserRankInfoDto(), IConstantsTest.PROMOTION_ID, IConstantsTest.LEADERBOARD_ID));
  }
}
