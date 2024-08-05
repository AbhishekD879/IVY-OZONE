package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SportsFeaturedTabDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SportsFeaturedTabMapper;
import com.ladbrokescoral.oxygen.cms.api.service.SportsFeaturedTabService;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class SportsFeaturedTabPublicService {

  private final SportsFeaturedTabService service;

  public SportsFeaturedTabPublicService(SportsFeaturedTabService service) {
    this.service = service;
  }

  public Optional<SportsFeaturedTabDto> getFeatureTabByPath(String brand, String path) {
    return service
        .findEnabledByBrandAndPath(brand, path)
        .map(SportsFeaturedTabMapper.INSTANCE::toDto);
  }
}
