package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.ShowOnDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ShowOn;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper
public interface ShowOnMapper {

  @Mapping(target = "routes", source = "showOn.routes")
  @Mapping(target = "sports", source = "sportsList")
  ShowOnDto toShowOnDto(ShowOn showOn, List<String> sportsList);
}
