package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardingGuideDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OnBoardingGuide;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {DateMapper.class, MapUtil.class})
public interface OnBoardingGuideMapper {

  OnBoardingGuideMapper INSTANCE = Mappers.getMapper(OnBoardingGuideMapper.class);

  OnBoardingGuideDto toDto(OnBoardingGuide entity);
}
