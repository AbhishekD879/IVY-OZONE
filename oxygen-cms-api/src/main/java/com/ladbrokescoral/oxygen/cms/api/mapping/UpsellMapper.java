package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.UpsellDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Upsell;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface UpsellMapper {
  static UpsellMapper getInstance() {
    return UpsellMapperInstance.INSTANCE;
  }

  @Mapping(
      target = "fallbackImagePath",
      expression =
          "java(source.getFallbackImage() != null? source.getFallbackImage().relativePath() : null)")
  UpsellDto toDto(Upsell source);

  final class UpsellMapperInstance {
    private static final UpsellMapper INSTANCE = Mappers.getMapper(UpsellMapper.class);

    private UpsellMapperInstance() {}
  }
}
