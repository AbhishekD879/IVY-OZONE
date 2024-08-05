package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.League;
import com.ladbrokescoral.oxygen.cms.api.repository.LeaguesRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class LeagueService extends SortableService<League> {

  private final LeaguesRepository leaguesRepository;

  @Autowired
  public LeagueService(final LeaguesRepository leaguesRepository) {
    super(leaguesRepository);
    this.leaguesRepository = leaguesRepository;
  }

  public List<League> findAllByBrandSorted(final String brand) {
    return leaguesRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
