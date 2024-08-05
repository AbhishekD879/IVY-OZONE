package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.entain.oxygen.promosandbox.dto.UserRankRequestDto;
import java.util.*;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

class UserRankServiceHelperTest {

  @Mock private SparkSession sparkSession;

  @InjectMocks private UserRankServiceHelper userRankServiceHelper;

  @BeforeEach
  void setUp() {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testFetchTopXRankPostivePositions() {
    UserRankRequestDto requestDto = createRequestDto("promo_123", "lb_456", null, 5, true);
    when(sparkSession.sql(anyString())).thenReturn(TestData.createMockDataset());
    List<Map<Object, Object>> result = userRankServiceHelper.fetchTopXRank(requestDto);
    assertNotNull(result);
  }

  @Test
  void testFetchTopXRankNoPositions() {
    UserRankRequestDto requestDto = createRequestDto("promo_123", "lb_456", null, 0, true);
    List<Map<Object, Object>> result = userRankServiceHelper.fetchTopXRank(requestDto);
    assertNotNull(result);
  }

  @Test
  void testFetchTopXRankRankingTrue() {
    UserRankRequestDto requestDto = createRequestDto("promo_123", "lb_456", null, 5, true);
    when(sparkSession.sql(anyString())).thenReturn(TestData.createMockDataset());
    List<Map<Object, Object>> result = userRankServiceHelper.fetchTopXRank(requestDto);
    assertNotNull(result);
  }

  @Test
  void testFetchIndividualRankByCustId() {
    UserRankRequestDto requestDto = createRequestDto("promo_123", "lb_123", "user_123", 0, true);
    when(sparkSession.sql(anyString())).thenReturn(TestData.createMockDataset());
    Map<Object, Object> result = userRankServiceHelper.fetchIndividualRank(requestDto);
    assertNotNull(result);
  }

  @Test
  void testFetchIndividualRankNonCustId() {
    UserRankRequestDto requestDto = createRequestDto("promo_123", "lb_345", "no user id ", 0, true);
    when(sparkSession.sql(anyString())).thenReturn(TestData.createEmptyDataset());
    Map<Object, Object> result = userRankServiceHelper.fetchIndividualRank(requestDto);
    assertNotNull(result);
  }

  @Test
  void testFetchIndividualRankForException() {
    UserRankRequestDto requestDto = createRequestDto("promo_123", "lb_456", "user_789", 0, true);
    when(sparkSession.sql(anyString()))
        .thenThrow(new NoSuchElementException("Customer does not exist."));
    Map<Object, Object> result = userRankServiceHelper.fetchIndividualRank(requestDto);
    assertNotNull(result);
  }

  @Test
  void testFetchIndividualRankCustRankingFalse() {
    UserRankRequestDto requestDto = createRequestDto("promo_123", "lb_456", "user_789", 0, false);

    Map<Object, Object> result = userRankServiceHelper.fetchIndividualRank(requestDto);
    assertNotNull(result);
    assertEquals(0, result.size());
  }

  private UserRankRequestDto createRequestDto(
      String promotionId,
      String leaderboardId,
      String customerId,
      int noOfPosition,
      boolean customerRanking) {
    UserRankRequestDto requestDto = new UserRankRequestDto();
    requestDto.setPromotionId(promotionId);
    requestDto.setLeaderboardId(leaderboardId);
    requestDto.setCustomerId(customerId);
    requestDto.setNoOfPosition(noOfPosition);
    requestDto.setCustomerRanking(customerRanking);
    return requestDto;
  }

  private static class TestData {
    private static final List<StructField> FIELDS =
        Arrays.asList(
            DataTypes.createStructField("customerId", DataTypes.StringType, false),
            DataTypes.createStructField("score", DataTypes.IntegerType, false));

    static Dataset<Row> createMockDataset() {
      List<Row> mockData = new ArrayList<>();
      mockData.add(RowFactory.create("user_1", 100));
      mockData.add(RowFactory.create("user_2", 200));
      StructType schema = DataTypes.createStructType(FIELDS);
      SparkSession spark =
          SparkSession.builder().appName("MockSparkSession").master("local").getOrCreate();
      return spark.createDataFrame(mockData, schema);
    }

    static Dataset<Row> createEmptyDataset() {
      StructType schema = DataTypes.createStructType(FIELDS);
      SparkSession spark =
          SparkSession.builder().appName("MockSparkSession").master("local").getOrCreate();
      return spark.createDataFrame(Collections.emptyList(), schema);
    }
  }
}
