package com.ladbrokescoral.oxygen.seo.dto;

import java.util.List;
import lombok.*;

@Data
@EqualsAndHashCode
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PromotionWithSectionContainerDto {
  private String expandedAmount;
  private List<PublicPromotionSectionDto> promotionsBySection;
}
