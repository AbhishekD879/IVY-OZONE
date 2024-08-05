package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class PromotionContainerDto<T> {
  private String expandedAmount;
  private List<T> promotions;
  private Map<String, List<PromotionDto>> promotionsBySection;
}
