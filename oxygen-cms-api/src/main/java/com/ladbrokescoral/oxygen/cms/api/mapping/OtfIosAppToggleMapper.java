package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.OtfIosAppToggleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OtfIosAppToggle;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface OtfIosAppToggleMapper {
  static OtfIosAppToggleMapper getInstance() {
    return OtfIosAppToggleMapper.OtfIOSAppToggleMapperSingleton.INSTANCE;
  }

  OtfIosAppToggleDto toDto(OtfIosAppToggle entity);

  @NoArgsConstructor(access = AccessLevel.PRIVATE)
  final class OtfIOSAppToggleMapperSingleton {
    private static final OtfIosAppToggleMapper INSTANCE =
        Mappers.getMapper(OtfIosAppToggleMapper.class);
  }
}
