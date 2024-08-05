package com.entain.oxygen.promosandbox.service;

import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.utils.PromoLbUtil;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.spark.sql.*;
import org.apache.spark.sql.types.StructField;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class RddCreationService {

  private final SparkSession sparkSession;

  @Autowired
  public RddCreationService(SparkSession sparkSession) {
    this.sparkSession = sparkSession;
  }

  public boolean createPromoUserRDD(
      UserRankInfoDto userRankData, String promotionId, String leaderboardId) {
    try {
      Long startTime = System.currentTimeMillis();
      Dataset<Row> dataset =
          sparkSession.createDataFrame(userRankData.getRowList(), userRankData.getStructType());
      Dataset<Row> totalPromoUsers = dataset.toDF().cache();
      totalPromoUsers.createOrReplaceTempView(
          "user_rank_table_" + promotionId + "_" + leaderboardId);
      Long endTime = System.currentTimeMillis();
      List<String> titleArray =
          Arrays.stream(userRankData.getStructType().fields())
              .map(StructField::name)
              .collect(Collectors.toList());
      log.info(
          "RDD Created : user_rank_table_{}_{} ,UserCount:{},columnTitle :{},TimeTaken(MILLISECOND) : {}",
          promotionId,
          leaderboardId,
          userRankData.getRowList().size(),
          titleArray,
          (endTime - startTime));
      PromoLbUtil.getPromoCsvTitleMap()
          .remove(PromoLbUtil.computePrimaryKey(promotionId, leaderboardId));
      return true;
    } catch (Exception ex) {
      log.error(
          "Error while loading user_rank_table_{}_{} data to spark cluster",
          promotionId,
          leaderboardId);
      return false;
    }
  }
}
