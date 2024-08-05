package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.CountrySettingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CountryData;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface CountryToCountrySettingsDtoMapper {

  CountryToCountrySettingsDtoMapper INSTANCE =
      Mappers.getMapper(CountryToCountrySettingsDtoMapper.class);

  CountrySettingDto toDto(CountryData source);
}
