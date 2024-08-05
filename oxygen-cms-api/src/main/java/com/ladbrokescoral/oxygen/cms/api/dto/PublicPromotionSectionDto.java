package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PublicPromotionSectionDto {

  private String brand;
  private List<PromotionDto> promotions;
  private String name;
  private Double sortOrder;
}
