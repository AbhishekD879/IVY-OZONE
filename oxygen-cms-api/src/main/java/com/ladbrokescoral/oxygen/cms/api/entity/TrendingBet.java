package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = false)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "trending-bets")
public class TrendingBet extends AbstractEntity implements HasBrand {
  @NotNull private String brand;

  @NotNull private String type;

  private Boolean active;
  private Boolean displayForAllUsers;
  private Boolean isQuickBetReceiptEnabled;

  private String mostBackedIn;
  private String eventStartsIn;

  @Min(value = 2, message = "The minimum value for maxSelections is 2")
  private Integer maxSelections;

  private Boolean isTimeInHours;
  private Integer betRefreshInterval;

  private boolean enableBackedUpTimes;
}
