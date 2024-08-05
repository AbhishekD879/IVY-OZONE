package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class FeatureContainerDto {
  private Integer expandedAmount;
  private List<FeatureDto> features;
}
