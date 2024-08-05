package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import java.util.Collection;
import java.util.Map;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SeoPageMapper {
  SeoPageMapper INSTANCE = Mappers.getMapper(SeoPageMapper.class);

  SeoPageDto toDto(SeoPage entity);

  static Map<String, String> toDto(Collection<SeoPage> entities) {
    return entities.stream()
        .collect(
            Collectors.toMap(
                SeoPage::getUrl, AbstractEntity::getId, (oldValue, newValue) -> newValue));
  }
}
