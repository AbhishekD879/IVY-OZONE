package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TemplateDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Template;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface TemplateMapper {

  TemplateMapper INSTANCE = Mappers.getMapper(TemplateMapper.class);

  @Mapping(
      target = "topRightCornerImagePath",
      expression =
          "java(source.getTopRightCornerImage() != null ? source.getTopRightCornerImage().relativePath() : null)")
  TemplateDto toDto(Template source);
}
