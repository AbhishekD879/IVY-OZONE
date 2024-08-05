package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionSectionDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class, DateMapper.class})
public interface PromotionSectionMapper {

  PromotionSectionMapper INSTANCE = Mappers.getMapper(PromotionSectionMapper.class);

  PromotionSection toInstance(PromotionSectionDto dto);
}
