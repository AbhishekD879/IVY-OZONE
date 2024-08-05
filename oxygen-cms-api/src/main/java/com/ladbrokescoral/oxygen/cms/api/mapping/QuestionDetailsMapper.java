package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QuestionDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuestionDetails;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuestionDetailsMapper {
  static QuestionDetailsMapper getInstance() {
    return QuestionDetailsMapperInstance.INSTANCE;
  }

  @Mapping(
      target = "homeTeamSvgFilePath",
      expression =
          "java(source.getHomeTeamSvg() != null ? source.getHomeTeamSvg().relativePath() : null)")
  @Mapping(
      target = "awayTeamSvgFilePath",
      expression =
          "java(source.getAwayTeamSvg() != null ? source.getAwayTeamSvg().relativePath() : null)")
  @Mapping(
      target = "channelSvgFilePath",
      expression =
          "java(source.getChannelSvg() != null ? source.getChannelSvg().relativePath() : null)")
  QuestionDetailsDto toDto(QuestionDetails source);

  final class QuestionDetailsMapperInstance {
    private static final QuestionDetailsMapper INSTANCE =
        Mappers.getMapper(QuestionDetailsMapper.class);

    private QuestionDetailsMapperInstance() {}
  }
}
