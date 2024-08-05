package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.ExternalLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExternalLink;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface ExternalLinkMapper {
  ExternalLinkMapper INSTANCE = Mappers.getMapper(ExternalLinkMapper.class);

  ExternalLinkDto toDto(ExternalLink entity);
}
