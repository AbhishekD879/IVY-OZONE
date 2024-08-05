package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LeagueDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LeaguePublicService;
import java.util.List;
import java.util.Objects;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LeaguesApi implements Public {

  private final LeaguePublicService leagueService;

  @Autowired
  public LeaguesApi(final LeaguePublicService leagueService) {
    this.leagueService = leagueService;
  }

  @GetMapping(value = "{brand}/leagues")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<LeagueDto> leagueDtos = leagueService.findByBrand(brand);
    return (Objects.isNull(leagueDtos) || leagueDtos.isEmpty())
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(leagueDtos, HttpStatus.OK);
  }
}
