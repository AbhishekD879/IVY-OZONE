package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.ladbrokescoral.oxygen.cms.client.model.PromotionContainerDto;
import com.ladbrokescoral.oxygen.cms.client.model.PromotionV2Dto;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class PromotionModuleDto extends CompetitionModuleDto {
  private PromotionContainerDto<PromotionV2Dto> promotionsData;
}
