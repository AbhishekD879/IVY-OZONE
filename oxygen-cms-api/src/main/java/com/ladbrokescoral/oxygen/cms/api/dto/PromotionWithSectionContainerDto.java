package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PromotionWithSectionContainerDto {
  private String expandedAmount;
  private List<PublicPromotionSectionDto> promotionsBySection;
}
