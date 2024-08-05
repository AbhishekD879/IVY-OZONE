package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import com.ladbrokescoral.oxygen.cms.api.repository.BybMarketRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class BybMarketService extends SortableService<BybMarket> {

  private final BybMarketRepository bybMarketRepository;

  @Autowired
  public BybMarketService(BybMarketRepository bybMarketRepository) {
    super(bybMarketRepository);
    this.bybMarketRepository = bybMarketRepository;
  }

  public List<BybMarket> findAllByBrandSorted(String brand) {
    return bybMarketRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }

  @Override
  protected boolean isNewElementCreatedFirstInTheList() {
    return false;
  }
}
