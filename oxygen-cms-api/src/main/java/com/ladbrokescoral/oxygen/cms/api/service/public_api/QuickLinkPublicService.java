package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.QuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.QuickLinkMapper;
import com.ladbrokescoral.oxygen.cms.api.service.QuickLinkService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class QuickLinkPublicService {

  private final QuickLinkService service;

  public QuickLinkPublicService(QuickLinkService service) {
    this.service = service;
  }

  public List<QuickLinkDto> findByBrand(String brand, String raceType) {
    return service.findAllByBrand(brand, raceType).stream()
        .map(QuickLinkMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
