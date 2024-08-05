package com.entain.oxygen.promosandbox.service;

import com.entain.oxygen.promosandbox.dto.UserRankRequestDto;
import com.entain.oxygen.promosandbox.utils.PromoLbUtil;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.StructField;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class UserRankServiceHelper {

  private final SparkSession sparkSession;

  @Autowired
  public UserRankServiceHelper(SparkSession sparkSession) {
    this.sparkSession = sparkSession;
  }

  @Cacheable(
      cacheNames = "topXRank",
      key =
          "#requestDto.promotionId.concat('-').concat(#requestDto.leaderboardId).concat('-').concat(#requestDto.noOfPosition)",
      unless = "#result.isEmpty()")
  public List<Map<Object, Object>> fetchTopXRank(UserRankRequestDto requestDto) {
    List<Map<Object, Object>> responseList = new ArrayList<>();
    if (requestDto.getNoOfPosition() > 0) {
      long fetchTopXRankStartTime = System.currentTimeMillis();
      Dataset<Row> topXDataSet =
          sparkSession.sql(
              "select * from user_rank_table_"
                  + requestDto.getPromotionId()
                  + "_"
                  + requestDto.getLeaderboardId()
                  + " limit "
                  + requestDto.getNoOfPosition());
      log.debug(
          "fetchTopXRank query time taken(MS) : {}  ",
          System.currentTimeMillis() - fetchTopXRankStartTime);
      List<String> schemaNames =
          PromoLbUtil.getRDDSchema(
              requestDto.getPromotionId(), requestDto.getLeaderboardId(), topXDataSet);
      long fetchTopXRankProcessingStartTime = System.currentTimeMillis();
      topXDataSet
          .collectAsList()
          .forEach(
              (Row row) -> {
                Map<Object, Object> userDataMap = new LinkedHashMap<>();
                schemaNames.forEach(name -> userDataMap.put(name, row.getAs(name).toString()));
                responseList.add(userDataMap);
              });
      log.debug(
          "fetchTopXRank processing time taken(MS) : {}  ",
          System.currentTimeMillis() - fetchTopXRankProcessingStartTime);
    }
    return responseList;
  }

  @Cacheable(
      cacheNames = "individualRank",
      key =
          "#requestDto.promotionId.concat('-').concat(#requestDto.leaderboardId).concat('-').concat(#requestDto.customerId).concat('-').concat(#requestDto.customerRanking)",
      unless = "#result.isEmpty()")
  public Map<Object, Object> fetchIndividualRank(UserRankRequestDto requestDto) {
    Map<Object, Object> individualRankMap = new LinkedHashMap<>();
    if (Boolean.TRUE.equals(requestDto.getCustomerRanking())) {
      try {
        long fetchIndividualRankQueryTime = System.currentTimeMillis();
        Row individualRank =
            sparkSession
                .sql(
                    "select * from user_rank_table_"
                        + requestDto.getPromotionId()
                        + "_"
                        + requestDto.getLeaderboardId()
                        + " where customerId='"
                        + requestDto.getCustomerId()
                        + "'")
                .first();
        log.debug(
            "fetchIndividualRank query time taken(MS) : {}  ",
            System.currentTimeMillis() - fetchIndividualRankQueryTime);
        long fetchIndividualRankProcessingTimeTaken = System.currentTimeMillis();
        for (StructField structField : individualRank.schema().fields()) {
          individualRankMap.put(
              structField.name(), individualRank.getAs(structField.name()).toString());
        }
        log.debug(
            "fetchIndividualRank processing time taken(MS) : {}  ",
            System.currentTimeMillis() - fetchIndividualRankProcessingTimeTaken);
      } catch (NoSuchElementException exception) {
        log.info(
            "User does not exist customerId : {} ,promotionId : {},leaderboardId:{}",
            requestDto.getCustomerId(),
            requestDto.getPromotionId(),
            requestDto.getLeaderboardId());
      }
    }
    return individualRankMap;
  }
}
