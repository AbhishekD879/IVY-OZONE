package com.entain.oxygen.promosandbox.dto;

import java.time.Instant;
import java.util.List;
import lombok.Data;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.types.StructType;

@Data
public class UserRankInfoDto {
  private List<Row> rowList;
  private StructType structType;
  private Instant lastFileModified;
}
