package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.League;
import com.ladbrokescoral.oxygen.cms.api.mapping.LeagueMapper;
import com.ladbrokescoral.oxygen.cms.api.service.LeagueService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class LeaguePublicService {

  private final LeagueService leagueService;

  public LeaguePublicService(final LeagueService leagueService) {
    this.leagueService = leagueService;
  }

  public List<LeagueDto> findByBrand(String brand) {
    List<League> leagueCollection = leagueService.findAllByBrandSorted(brand);
    return leagueCollection.stream().map(LeagueMapper.INSTANCE::toDto).collect(Collectors.toList());
  }
}
