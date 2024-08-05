package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetModuleData;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetModuleDto;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface BybWidgetMapper {

  BybWidgetModuleDto toDto(BybWidgetDto entity);

  BybWidgetModuleData toDtoData(BybWidgetDataDto data);
}
