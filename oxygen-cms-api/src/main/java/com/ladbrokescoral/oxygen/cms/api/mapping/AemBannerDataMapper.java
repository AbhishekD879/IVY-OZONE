package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.AemBannersDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportPageId;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface AemBannerDataMapper {
  AemBannerDataMapper INSTANCE = Mappers.getMapper(AemBannerDataMapper.class);

  @Mapping(target = "sportPageId", expression = "java(createSportPageId(entity))")
  @Mapping(target = "maxOffers", source = "entity.moduleConfig.maxOffers")
  @Mapping(target = "timePerSlide", source = "entity.moduleConfig.timePerSlide")
  @Mapping(target = "displayFrom", source = "entity.moduleConfig.displayFrom")
  @Mapping(target = "displayTo", source = "entity.moduleConfig.displayTo")
  AemBannersDto toDto(SportModule entity);

  default SportPageId createSportPageId(SportModule entity) {
    return SportPageId.fromSportModule(entity);
  }
}
