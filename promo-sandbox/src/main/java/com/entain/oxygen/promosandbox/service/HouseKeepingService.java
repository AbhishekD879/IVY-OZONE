package com.entain.oxygen.promosandbox.service;

import lombok.extern.slf4j.Slf4j;
import org.apache.spark.sql.SparkSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class HouseKeepingService {

  private final SparkSession sparkSession;

  @Autowired
  public HouseKeepingService(SparkSession sparkSession) {
    this.sparkSession = sparkSession;
  }

  public boolean dropSparkTempTable(String promotionId, String leaderboardId) {
    try {
      sparkSession
          .sqlContext()
          .dropTempTable("user_rank_table_" + promotionId + "_" + leaderboardId);
      log.info(
          "RDD user_rank_table_"
              + promotionId
              + "_"
              + leaderboardId
              + " Deleted from spark cluster");
      return true;
    } catch (Exception e) {
      log.error("Error while dropping user_rank_table_{}_{}", promotionId, leaderboardId);
      return false;
    }
  }
}
