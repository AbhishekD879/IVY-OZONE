package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.EventDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.EventDetails;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuizEventDetailsMapper {
  static QuizEventDetailsMapper getInstance() {
    return QuizEventDetailsMapperInstance.INSTANCE;
  }

  @Mapping(target = "liveNow", expression = "java(source.isLiveNow())")
  EventDetailsDto toDto(EventDetails source);

  final class QuizEventDetailsMapperInstance {
    private static final QuizEventDetailsMapper INSTANCE =
        Mappers.getMapper(QuizEventDetailsMapper.class);

    private QuizEventDetailsMapperInstance() {}
  }
}
