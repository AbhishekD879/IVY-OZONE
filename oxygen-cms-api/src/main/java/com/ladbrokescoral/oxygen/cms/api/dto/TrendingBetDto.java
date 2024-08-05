package com.ladbrokescoral.oxygen.cms.api.dto;

import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TrendingBetDto {
  private String id;
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
