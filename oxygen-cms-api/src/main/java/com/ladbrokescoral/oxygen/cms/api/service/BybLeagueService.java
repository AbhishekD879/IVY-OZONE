package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BybLeague;
import com.ladbrokescoral.oxygen.cms.api.repository.BybLeagueRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class BybLeagueService extends SortableService<BybLeague> {

  private final BybLeagueRepository bybLeagueRepository;

  @Autowired
  public BybLeagueService(BybLeagueRepository bybLeagueRepository) {
    super(bybLeagueRepository);
    this.bybLeagueRepository = bybLeagueRepository;
  }

  public List<BybLeague> findAllByBrandSorted(String brand) {
    return bybLeagueRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
