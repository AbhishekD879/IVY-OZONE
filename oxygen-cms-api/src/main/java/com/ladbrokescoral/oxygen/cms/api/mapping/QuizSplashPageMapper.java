package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SplashPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.SplashPage;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuizSplashPageMapper {

  static QuizSplashPageMapper getInstance() {
    return QuizSplashPageMapperInstance.INSTANCE;
  }

  @Mapping(target = "backgroundSvgFilePath", expression = "java(source.backgroundSvgPath())")
  @Mapping(target = "logoSvgFilePath", expression = "java(source.logoSvgPath())")
  @Mapping(target = "footerSvgFilePath", expression = "java(source.footerSvgPath())")
  SplashPageDto toDto(SplashPage source);

  final class QuizSplashPageMapperInstance {
    private static final QuizSplashPageMapper INSTANCE =
        Mappers.getMapper(QuizSplashPageMapper.class);

    private QuizSplashPageMapperInstance() {}
  }
}
