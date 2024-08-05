package com.entain.oxygen.promosandbox.dto;

import javax.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserRankRequestDto {
  @NotBlank private String promotionId;
  private String customerId;
  private Boolean customerRanking = Boolean.FALSE;
  private Integer noOfPosition;
  @NotBlank private String leaderboardId;

  @Override
  public String toString() {
    return "{"
        + "promotionId='"
        + promotionId
        + '\''
        + ", customerId='"
        + customerId
        + '\''
        + ", customerRanking='"
        + customerRanking
        + '\''
        + ", leaderboardId='"
        + leaderboardId
        + '\''
        + ", noOfPosition="
        + noOfPosition
        + '}';
  }
}
