package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
import com.ladbrokescoral.oxygen.cms.api.repository.impl.MarketLinkRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MarketLinkService extends AbstractService<MarketLink> {
  private final MarketLinkRepository marketLinkRepository;

  @Autowired
  public MarketLinkService(MarketLinkRepository marketLinkRepository) {
    super(marketLinkRepository);
    this.marketLinkRepository = marketLinkRepository;
  }

  public List<MarketLink> getMarketLinksByBrand(String brand) {
    return marketLinkRepository.findByBrandEqualsAndEnabledTrue(brand);
  }
}
