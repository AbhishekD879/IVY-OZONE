package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.StaticBlockMapper;
import com.ladbrokescoral.oxygen.cms.api.service.StaticBlockService;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class StaticBlockPublicService {

  private final StaticBlockService service;

  public StaticBlockPublicService(StaticBlockService service) {
    this.service = service;
  }

  public Optional<StaticBlockDto> find(String brand, String uri) {
    return service.findByBrandAndUri(brand, uri).map(StaticBlockMapper.INSTANCE::toDto);
  }
}
