package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupSettingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuizPopupGeneralSettingMapper {
  QuizPopupGeneralSettingMapper INSTANCE = Mappers.getMapper(QuizPopupGeneralSettingMapper.class);

  QuizPopupSettingDto toDto(QuizPopupSetting entity);
}
