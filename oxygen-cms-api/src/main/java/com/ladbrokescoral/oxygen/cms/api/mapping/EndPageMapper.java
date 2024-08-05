package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.EndPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.EndPage;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface EndPageMapper {
  static EndPageMapper getInstance() {
    return EndPageMapper.EndPageMapperInstance.INSTANCE;
  }

  @Mapping(
      target = "backgroundSvgImagePath",
      expression =
          "java(source.getBackgroundSvgImage() != null? source.getBackgroundSvgImage().relativePath() : null)")
  EndPageDto toDto(EndPage source);

  final class EndPageMapperInstance {
    private static final EndPageMapper INSTANCE = Mappers.getMapper(EndPageMapper.class);

    private EndPageMapperInstance() {}
  }
}
