package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class CompetitionPublicService {

  private final CompetitionService competitionService;

  public CompetitionPublicService(CompetitionService competitionService) {
    this.competitionService = competitionService;
  }

  public List<Competition> readAllByBrand(String brand) {
    return competitionService.findByBrand(brand);
  }

  public Competition readByBrandAndUri(String brand, String uri) {
    return competitionService
        .getCompetitionByBrandAndUri(brand, uri)
        .orElseThrow(NotFoundException::new);
  }
}
