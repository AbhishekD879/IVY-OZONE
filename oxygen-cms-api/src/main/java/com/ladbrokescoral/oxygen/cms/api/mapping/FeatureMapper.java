package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.FeatureDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import com.ladbrokescoral.oxygen.cms.api.mapping.FeatureMapUtil.FeatureMapUtils;
import com.ladbrokescoral.oxygen.cms.api.mapping.FeatureMapUtil.ShowToCustomer;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.MapUtils;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.UriSubstring;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class, DateMapper.class, FeatureMapUtil.class})
public interface FeatureMapper {
  FeatureMapper INSTANCE = Mappers.getMapper(FeatureMapper.class);

  @Mapping(target = "filename", source = "entity.filename.filename")
  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "showToCustomer",
      qualifiedBy = {FeatureMapUtils.class, ShowToCustomer.class})
  FeatureDto toDto(Feature entity);
}
