package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerTabletDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.BetReceiptBannerMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.BetReceiptBannerTabletService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class BetReceiptBannerTabletPublicService implements ApiService<BetReceiptBannerTabletDto> {

  private final BetReceiptBannerTabletService service;

  public BetReceiptBannerTabletPublicService(BetReceiptBannerTabletService service) {
    this.service = service;
  }

  public List<BetReceiptBannerTabletDto> findByBrand(String brand) {
    return service.findAllByBrand(brand).stream()
        .map(BetReceiptBannerMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
