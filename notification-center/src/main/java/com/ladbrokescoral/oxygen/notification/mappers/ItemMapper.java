package com.ladbrokescoral.oxygen.notification.mappers;

import com.ladbrokescoral.oxygen.notification.entities.Item;
import com.ladbrokescoral.oxygen.notification.entities.dto.ItemDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Mappings;

@Mapper
public interface ItemMapper {

  @Mappings({@Mapping(target = "type", ignore = true), @Mapping(target = "id", ignore = true)})
  ItemDTO toItemDTO(Item item);
}
