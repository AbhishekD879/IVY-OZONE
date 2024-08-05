package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import com.ladbrokescoral.oxygen.cms.api.mapping.BybMarketMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.BybMarketService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class BybMarketPublicService implements ApiService<BybMarketDto> {

  private final BybMarketService service;

  public BybMarketPublicService(BybMarketService service) {
    this.service = service;
  }

  public List<BybMarketDto> findByBrand(String brand) {
    List<BybMarket> bybMarkets = service.findAllByBrandSorted(brand);
    return bybMarkets.stream().map(BybMarketMapper.INSTANCE::toDto).collect(Collectors.toList());
  }
}
