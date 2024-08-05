package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuizPopup;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuizPopupMapper {
  static QuizPopupMapper getInstance() {
    return QuizPopupMapperInstance.INSTANCE;
  }

  @Mapping(
      target = "iconSvgPath",
      expression = "java(source.getIcon() != null ? source.getIcon().relativePath() : null)")
  QuizPopupDto toDto(QuizPopup source);

  final class QuizPopupMapperInstance {
    private static final QuizPopupMapper INSTANCE = Mappers.getMapper(QuizPopupMapper.class);

    private QuizPopupMapperInstance() {}
  }
}
