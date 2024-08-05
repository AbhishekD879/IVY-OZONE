package com.entain.oxygen.promosandbox.utils;

import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.model.PromoConfig;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.Row$;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.Metadata;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import scala.collection.JavaConverters;

public class RequestUtilHelper {

  public static UserRankInfoDto prepareUserRankInfo() {
    List<Map<String, String>> dataList = new ArrayList<>();
    Map<String, String> dataMap = new HashMap<>();
    dataList.add(dataMap);
    dataMap.put("customerId", "12311");
    List<String> cols = new ArrayList<>();
    cols.add("customerId");
    List<Row> rows = prepareRows(dataList, cols);
    StructType fieldSchema =
        new StructType(
            cols.stream()
                .map(c -> new StructField(c, DataTypes.StringType, true, Metadata.empty()))
                .toArray(StructField[]::new));
    UserRankInfoDto userRankInfoDto = new UserRankInfoDto();
    userRankInfoDto.setStructType(fieldSchema);
    userRankInfoDto.setRowList(rows);
    return userRankInfoDto;
  }

  public static List<Row> prepareRows(List<Map<String, String>> dataList, List<String> cols) {
    return dataList
        .parallelStream()
        .map(row -> cols.stream().map(c -> (Object) row.get(c)))
        .map(row -> row.collect(Collectors.toList()))
        .map(row -> JavaConverters.asScalaBufferConverter(row).asScala().toSeq())
        .map(Row$.MODULE$::fromSeq)
        .collect(Collectors.toList());
  }

  public static List<PromoConfig> getPromoConfigs(PromoConfig promoConfig) {
    return new ArrayList<PromoConfig>() {
      {
        add(promoConfig);
      }
    };
  }
}
