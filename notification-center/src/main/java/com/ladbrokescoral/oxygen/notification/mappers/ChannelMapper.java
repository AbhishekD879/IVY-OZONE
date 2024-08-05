package com.ladbrokescoral.oxygen.notification.mappers;

import com.ladbrokescoral.oxygen.notification.entities.dto.ChannelDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.ItemDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Mappings;

@Mapper
public interface ChannelMapper {
  @Mappings({
    @Mapping(
        target = "name",
        expression = "java(String.format(item.getType() + \"%010d\", item.getEventId()))"),
    @Mapping(target = "expiration", ignore = true)
  })
  ChannelDTO toChannelDTO(ItemDTO item);
}
