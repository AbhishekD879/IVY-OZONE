package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataSportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataSportCategorySegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialSportConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialSportConfigDto.SSRequestFilters;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialSportPageConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryNativeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsCardHeaderType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.ObjectUtils;

@Mapper(uses = {MapUtil.class})
public interface SportCategoryMapper extends SegmentReferenceMapper {

  SportCategoryMapper INSTANCE = Mappers.getMapper(SportCategoryMapper.class);

  @Mapping(
      target = "uriSmall",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriLarge",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriSmallIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriMediumIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriLargeIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  @Mapping(target = "filename", source = "entity.filename.filename")
  @Mapping(target = "scoreBoardUrl", source = "scoreBoardUri")
  @Mapping(target = "sportConfig", source = "entity")
  SportCategoryDto toDto(SportCategory entity);

  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  @Mapping(target = "scoreBoardUrl", source = "scoreBoardUri")
  @Mapping(target = "sportConfig", source = "entity")
  InitialDataSportCategoryDto toInitialDto(SportCategory entity);

  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  @Mapping(target = "scoreBoardUrl", source = "scoreBoardUri")
  @Mapping(target = "sportConfig", source = "entity")
  InitialDataSportCategorySegmentedDto toInitialSegmentedDto(SportCategory entity);

  @Mapping(
      target = "uriSmall",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriLarge",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriSmallIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriMediumIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriLargeIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  @Mapping(target = "filename", source = "entity.filename.filename")
  @Mapping(target = "scoreBoardUrl", source = "scoreBoardUri")
  SportCategoryNativeDto toDtoNative(SportCategory entity);

  @Mapping(target = "title", source = "imageTitle")
  @Mapping(
      target = "path",
      source = "targetUri",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.PathFromUri.class})
  @Mapping(
      target = "name",
      source = "targetUri",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NameFromUri.class})
  @Mapping(target = "request", source = "entity")
  InitialSportConfigDto toInitialSport(SportCategory entity);

  default InitialSportPageConfigDto toInitialSportPage(SportCategory entity) {
    InitialSportPageConfigDto pageConfigDto = new InitialSportPageConfigDto();
    if (!ObjectUtils.isEmpty(entity)) {
      pageConfigDto.setConfig(toInitialSport(entity));
    }
    return pageConfigDto;
  }

  default Integer map(SportTier tier) {
    return tier != null ? tier.value : null;
  }

  default String map(OddsCardHeaderType type) {
    return type == null ? "" : type.value;
  }

  default SSRequestFilters map(SportCategory sportCategory) {
    SSRequestFilters filters = new SSRequestFilters();
    filters.setCategoryId(String.valueOf(sportCategory.getCategoryId()));
    filters.setMarketsCount(!sportCategory.isOutrightSport());
    filters.setAggregatedMarkets(sportCategory.getAggrigatedMarkets());

    if (!sportCategory.isOutrightSport()) {
      filters.setMarketTemplateMarketNameIntersects(sportCategory.getPrimaryMarkets());

      if (sportCategory.getDispSortNames() != null) {
        String[] dispSortNameFilters = MapUtil.namesToArray(sportCategory.getDispSortNames());
        filters.setDispSortName(dispSortNameFilters);
        filters.setDispSortNameIncludeOnly(dispSortNameFilters);
      }
    }
    return filters;
  }

  default InitialDataSportCategorySegmentedDto toDto(
      SportCategory sportCategory, List<String> segments) {
    InitialDataSportCategorySegmentedDto initialDataSportCategoryDto =
        toInitialSegmentedDto(sportCategory);
    return toSegmentedDto(sportCategory, initialDataSportCategoryDto, segments);
  }

  @Mapping(target = "segmentReferences", ignore = true)
  @Mapping(target = "segments", ignore = true)
  InitialDataSportCategorySegmentedDto toSegmentedDto(SportCategory entity);

  default InitialDataSportCategorySegmentedDto toSegmentedDto(
      SportCategory entity,
      InitialDataSportCategorySegmentedDto initialDataSportCategoryDto,
      List<String> segments) {
    initialDataSportCategoryDto.setSegments(getSegments(entity, segments));
    initialDataSportCategoryDto.setSegmentReferences(getSegmentReferences(entity));
    initialDataSportCategoryDto.setUniversalSegment(entity.isUniversalSegment());
    return initialDataSportCategoryDto;
  }
}
