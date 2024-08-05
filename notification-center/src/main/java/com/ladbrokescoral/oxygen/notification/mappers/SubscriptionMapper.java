package com.ladbrokescoral.oxygen.notification.mappers;

import com.ladbrokescoral.oxygen.notification.entities.dto.ItemDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Mappings;

@Mapper(imports = {Platform.class})
public interface SubscriptionMapper {
  @Mappings({
    @Mapping(target = "platform", expression = "java(Platform.get(item.getPlatform()))"),
    @Mapping(target = "ownerId", ignore = true),
    @Mapping(target = "sentNonRunners", ignore = true)
  })
  SubscriptionDTO toSubscriptionDTO(ItemDTO item);
}
