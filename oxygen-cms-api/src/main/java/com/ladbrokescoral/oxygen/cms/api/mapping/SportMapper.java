package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataSportDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportOddsCardHeaderTypeDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportTabsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.MapUtils;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.NullToEmpty;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.StringToList;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.UriSubstring;
import java.util.Arrays;
import org.mapstruct.AfterMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class})
public interface SportMapper {

  SportMapper INSTANCE = Mappers.getMapper(SportMapper.class);

  @Mapping(
      target = "uriSmall",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "uriLarge",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "uriSmallIcon",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "uriMediumIcon",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "uriLargeIcon",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtils.class, NullToEmpty.class})
  @Mapping(target = "filename", source = "entity.filename.filename")
  @Mapping(target = "viewByFilters", ignore = true)
  @Mapping(target = "oddsCardHeaderType", ignore = true)
  @Mapping(target = "tabs", ignore = true)
  @Mapping(
      target = "typeIds",
      source = "entity.typeIds",
      qualifiedBy = {MapUtils.class, StringToList.class})
  @Mapping(
      target = "dispSortName",
      source = "dispSortName",
      qualifiedBy = {MapUtils.class, StringToList.class})
  SportDto toDto(Sport entity);

  SportOddsCardHeaderTypeDto toDtoOdds(Sport entity);

  @Mapping(target = "tabLive", source = "entity.tabLive")
  @Mapping(target = "tabMatches", source = "entity.tabMatches")
  @Mapping(target = "tabOutrights", source = "entity.tabOutrights")
  @Mapping(target = "tabSpecials", source = "entity.tabSpecials")
  SportTabsDto toDtoTabs(Sport entity);

  @AfterMapping
  default void mapNestedObjects(Sport source, @MappingTarget SportDto target) {
    target.setOddsCardHeaderType(toDtoOdds(source));
    target.setTabs(toDtoTabs(source));
    target.setViewByFilters(Arrays.asList("byCompetitions", "byTime"));
  }

  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtils.class, NullToEmpty.class})
  @Mapping(target = "oddsCardHeaderType", ignore = true)
  @Mapping(target = "tabs", ignore = true)
  @Mapping(
      target = "typeIds",
      source = "typeIds",
      qualifiedBy = {MapUtils.class, StringToList.class})
  @Mapping(
      target = "dispSortName",
      source = "dispSortName",
      qualifiedBy = {MapUtils.class, StringToList.class})
  InitialDataSportDto toInitialDto(Sport sport);
}
