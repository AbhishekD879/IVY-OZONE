package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizConfigurationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuizConfiguration;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuizConfigurationMapper {
  static QuizConfigurationMapper getInstance() {
    return QuizConfigurationMapperInstance.INSTANCE;
  }

  QuizConfigurationDto toDto(QuizConfiguration source);

  final class QuizConfigurationMapperInstance {
    private static final QuizConfigurationMapper INSTANCE =
        Mappers.getMapper(QuizConfigurationMapper.class);

    private QuizConfigurationMapperInstance() {}
  }
}
