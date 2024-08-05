package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.Data;

@Data
public class RGYConfigRequest {
  private String brand;
  private int reasonCode;
  private int riskLevelCode;
  private String riskLevelDesc;
  private String reasonDesc;

  @JsonProperty("enabled")
  private boolean bonusSuppression;

  private List<String> moduleIds;
}
