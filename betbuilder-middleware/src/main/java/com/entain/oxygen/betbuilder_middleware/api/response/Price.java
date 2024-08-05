package com.entain.oxygen.betbuilder_middleware.api.response;

import java.util.List;
import lombok.Data;

@Data
public class Price {
  private String batchId;
  private String combinationId;
  private String sgpId;
  private Integer providerId;
  private Integer status;
  private Integer errorCode;
  private String errorMessage;
  private Double truePrice;
  private Odds odds;
  private Integer suspensionState;
  private List<LegInformation> legInformation;
}
