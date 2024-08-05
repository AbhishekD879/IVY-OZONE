package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.YcLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.YcLeagueMapper;
import com.ladbrokescoral.oxygen.cms.api.service.YourCallLeagueService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

@Service
public class YourCallLeaguePublicService {

  private final YourCallLeagueService service;

  public YourCallLeaguePublicService(YourCallLeagueService service) {
    this.service = service;
  }

  public List<YcLeagueDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findAllByBrandSorted(brand).stream()
        .map(YcLeagueMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
