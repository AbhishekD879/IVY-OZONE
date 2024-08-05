package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface AliasModuleNamesMapper {

  public static AliasModuleNamesMapper MAPPER = Mappers.getMapper(AliasModuleNamesMapper.class);

  AliasModuleNamesDto toQLDto(SportQuickLink quickLink);

  AliasModuleNamesDto toSBDto(NavigationPoint navigationPoint);

  AliasModuleNamesDto toSSBDto(ExtraNavigationPoint extraNavigationPoint);
}
