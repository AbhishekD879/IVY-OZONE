package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.BybLeagueMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.BybLeagueService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

@Service
public class BybLeaguePublicService implements ApiService<BybLeagueDto> {

  private final BybLeagueService service;

  public BybLeaguePublicService(BybLeagueService service) {
    this.service = service;
  }

  public List<BybLeagueDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findAllByBrandSorted(brand).stream()
        .map(BybLeagueMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
