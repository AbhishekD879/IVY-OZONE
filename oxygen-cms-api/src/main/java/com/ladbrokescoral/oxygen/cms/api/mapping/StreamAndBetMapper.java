package com.ladbrokescoral.oxygen.cms.api.mapping;

import static com.ladbrokescoral.oxygen.cms.api.mapping.StreamAndBetMapUtil.*;

import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventTreeNodeDto;
import com.ladbrokescoral.oxygen.cms.api.dto.StreamAndBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBetShortNode;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {StreamAndBetMapUtil.class, WidgetMapUtil.class})
public interface StreamAndBetMapper {
  StreamAndBetMapper INSTANCE = Mappers.getMapper(StreamAndBetMapper.class);

  StreamAndBetDto toDto(StreamAndBet entity);

  @Mapping(target = "id", source = "siteServeId")
  @Mapping(
      target = "androidActive",
      source = "showItemFor",
      qualifiedBy = {StreamAndBetUtils.class, AndroidActive.class})
  @Mapping(
      target = "iosActive",
      source = "showItemFor",
      qualifiedBy = {StreamAndBetUtils.class, IOSActive.class})
  StreamAndBetDto.SABChildElementDto toDto(StreamAndBet.SABChildElement entity);

  @Mapping(target = "id", source = "classId")
  @Mapping(target = "name", source = "className")
  StreamAndBetShortNode toClassDto(SiteServeEventTreeNodeDto entity);

  @Mapping(target = "id", source = "typeId")
  @Mapping(target = "name", source = "typeName")
  StreamAndBetShortNode toTypeDto(SiteServeEventTreeNodeDto entity);

  @Mapping(target = "id", source = "id")
  @Mapping(target = "name", source = "name")
  StreamAndBetShortNode toEventDto(SiteServeEventTreeNodeDto entity);
}
