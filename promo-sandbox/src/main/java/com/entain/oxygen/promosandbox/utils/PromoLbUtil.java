package com.entain.oxygen.promosandbox.utils;

import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import java.util.*;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.types.StructField;

public class PromoLbUtil {

  private PromoLbUtil() {}

  private static final Map<String, List<String>> promoCsvTitleMap = new HashMap<>();

  public static Map<String, List<String>> getPromoCsvTitleMap() {
    return promoCsvTitleMap;
  }

  public static List<String> getRDDSchema(
      String promotionId, String leaderboardId, Dataset<Row> dataset) {
    return promoCsvTitleMap.computeIfAbsent(
        computePrimaryKey(promotionId, leaderboardId), v -> computeValue(dataset));
  }

  public static List<String> computeValue(Dataset<Row> dataset) {
    List<String> schemaList = new ArrayList<>();
    StructField[] schemeDetails = dataset.schema().fields();
    for (StructField structField : schemeDetails) {
      schemaList.add(structField.name());
    }
    return schemaList;
  }

  public static String computePrimaryKey(String promoId, String lbId) {
    return promoId + "_" + lbId;
  }

  public static boolean isDataExist(UserRankInfoDto userRankDetails) {
    return Objects.nonNull(userRankDetails.getRowList())
        && !userRankDetails.getRowList().isEmpty()
        && Objects.nonNull(userRankDetails.getStructType());
  }
}
