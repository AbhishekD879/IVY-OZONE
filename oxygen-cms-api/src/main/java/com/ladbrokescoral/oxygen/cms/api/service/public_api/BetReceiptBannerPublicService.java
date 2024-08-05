package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.BetReceiptBannerMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.BetReceiptBannerService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class BetReceiptBannerPublicService implements ApiService<BetReceiptBannerDto> {

  private final BetReceiptBannerService service;

  public BetReceiptBannerPublicService(BetReceiptBannerService service) {
    this.service = service;
  }

  public List<BetReceiptBannerDto> findByBrand(String brand) {
    return service.findAllByBrand(brand).stream()
        .map(BetReceiptBannerMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
