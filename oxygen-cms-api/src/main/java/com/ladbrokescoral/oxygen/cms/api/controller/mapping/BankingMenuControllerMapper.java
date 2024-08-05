package com.ladbrokescoral.oxygen.cms.api.controller.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.BankingMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface BankingMenuControllerMapper {

  BankingMenuControllerMapper INSTANCE = Mappers.getMapper(BankingMenuControllerMapper.class);

  @Mapping(target = "createdBy", ignore = true)
  @Mapping(target = "createdByUserName", ignore = true)
  @Mapping(target = "updatedBy", ignore = true)
  @Mapping(target = "updatedByUserName", ignore = true)
  @Mapping(target = "createdAt", ignore = true)
  @Mapping(target = "updatedAt", ignore = true)
  BankingMenu toEntity(BankingMenuDto entity);
}
