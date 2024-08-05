package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostConfigEntity;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface OddsBoostConfigurationMapper {
  OddsBoostConfigurationMapper INSTANCE = Mappers.getMapper(OddsBoostConfigurationMapper.class);

  @Mapping(target = "enabled", source = "enabled")
  @Mapping(target = "loggedOutHeaderText", source = "loggedOutHeaderText")
  @Mapping(target = "loggedInHeaderText", source = "loggedInHeaderText")
  @Mapping(target = "termsAndConditionsText", source = "termsAndConditionsText")
  @Mapping(target = "svgId", source = "svgId")
  @Mapping(target = "svg", source = "svg")
  @Mapping(target = "moreLink", source = "moreLink")
  @Mapping(
      target = "svgFilename",
      expression =
          "java(entity.getSvgFilename() != null ? entity.getSvgFilename().getFilename() : null)")
  @Mapping(target = "lang", source = "lang")
  @Mapping(target = "countDownTimer", source = "countDownTimer")
  @Mapping(target = "noTokensText", source = "noTokensText")
  OddsBoostConfigDTO toDTO(OddsBoostConfigEntity entity);
}
