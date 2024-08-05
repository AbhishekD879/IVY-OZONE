package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoAutoInitDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeoAutoPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import java.util.Collection;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;
import org.springframework.stereotype.Component;

@Mapper
@Component
public interface SeoAutoPageMapper {

  SeoAutoPageMapper INSTANCE = Mappers.getMapper(SeoAutoPageMapper.class);

  SeoAutoPageDto toDto(SeoAutoPage entity);

  SeoAutoPage toEntity(SeoAutoPageDto entity);

  static Map<String, SeoAutoInitDataDto> toDto(Collection<SeoAutoPage> entities) {
    return entities.stream()
        .filter(Objects::nonNull)
        .collect(
            Collectors.toMap(
                SeoAutoPage::getUri,
                SeoAutoInitDataDtoMapper.INSTANCE::toInitDataDto,
                (oldValue, newValue) -> newValue));
  }
}
