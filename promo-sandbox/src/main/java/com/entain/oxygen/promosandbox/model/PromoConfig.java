package com.entain.oxygen.promosandbox.model;

import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "promoConfig")
@Data
@ToString
@EqualsAndHashCode(callSuper = false)
public class PromoConfig extends AbstractEntity {
  @Id private String id;
  private String leaderboardId;
  private String promotionId;
  private String brand;
  private Instant startDate;
  private Instant endDate;
  private String filePath;
  private String fileProcessStatus;
  private Integer noOfRecord;
  private boolean isDataCleaned;
  private Instant lastFileModified;
}
