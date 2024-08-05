package com.ladbrokescoral.oxygen.questionengine.dto.crm;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class CoinResponse {

  private String rewardValue;
  private String rewardStatus;
  private String rewardErrorCode;
  private String commStatus;
  private String commErrorCode;
  private String requestReferenceId;
  private String transactionReferenceId;
}
