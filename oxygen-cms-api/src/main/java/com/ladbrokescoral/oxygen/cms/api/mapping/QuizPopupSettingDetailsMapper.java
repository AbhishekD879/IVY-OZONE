package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupSettingDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuizPopupSettingDetailsMapper {
  QuizPopupSettingDetailsMapper INSTANCE = Mappers.getMapper(QuizPopupSettingDetailsMapper.class);

  QuizPopupSettingDetailsDto toDto(QuizPopupSetting entity);
}
