package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface LuckyDipMapper {

  static LuckyDipMapper getInstance() {
    return LuckyDipMapperInstance.LD_INSTANCE;
  }

  LuckyDipModuleDto toDto(SportModule entity);

  LuckyDipModuleDto copy(LuckyDipModuleDto luckyDipDto);

  final class LuckyDipMapperInstance {
    private static final LuckyDipMapper LD_INSTANCE = Mappers.getMapper(LuckyDipMapper.class);

    private LuckyDipMapperInstance() {}
  }
}
