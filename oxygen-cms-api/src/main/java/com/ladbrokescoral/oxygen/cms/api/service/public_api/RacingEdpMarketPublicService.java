package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RacingEdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.controller.mapping.RacingEdpMarketsMapper;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import com.ladbrokescoral.oxygen.cms.api.service.RacingEdpMarketService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class RacingEdpMarketPublicService {

  private final RacingEdpMarketService service;

  public RacingEdpMarketPublicService(RacingEdpMarketService service) {
    this.service = service;
  }

  public List<RacingEdpMarketDto> findByBrand(String brand) {
    List<RacingEdpMarket> racingEdpMarkets = service.findAllByBrandSorted(brand);
    return racingEdpMarkets.stream()
        .map(RacingEdpMarketsMapper.ENTITY_MAPPER::toDto)
        .collect(Collectors.toList());
  }
}
