package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerTabletDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBanner;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBannerTablet;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {DateMapper.class})
public interface BetReceiptBannerMapper {
  BetReceiptBannerMapper INSTANCE = Mappers.getMapper(BetReceiptBannerMapper.class);

  BetReceiptBannerTabletDto toDto(BetReceiptBannerTablet entity);

  BetReceiptBannerDto toDto(BetReceiptBanner entity);
}
