package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.EdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.EdpMarket;
import com.ladbrokescoral.oxygen.cms.api.mapping.EdpMarketMapper;
import com.ladbrokescoral.oxygen.cms.api.service.EdpMarketService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class EdpMarketPublicService {

  private final EdpMarketService service;

  public EdpMarketPublicService(EdpMarketService service) {
    this.service = service;
  }

  public List<EdpMarketDto> findByBrand(String brand) {
    List<EdpMarket> edpMarketCollection = service.findAllByBrandSorted(brand);
    return edpMarketCollection.stream()
        .map(EdpMarketMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
