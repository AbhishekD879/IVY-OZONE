package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.*;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface PopularAccaWidgetMapper {

  PopularAccaModuleDto toDto(PopularAccaWidgetDto entity);

  PopularAccaModuleData toDtoData(PopularAccaWidgetDataDto data);
}
