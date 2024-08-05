package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.YcStaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.YcStaticBlockMapper;
import com.ladbrokescoral.oxygen.cms.api.service.YourCallStaticBlockService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class YourCallStaticBlockPublicService {

  private final YourCallStaticBlockService service;

  public YourCallStaticBlockPublicService(YourCallStaticBlockService service) {
    this.service = service;
  }

  public List<YcStaticBlockDto> findByBrand(String brand) {
    return service.findByBrandAndEnabled(brand).stream()
        .map(YcStaticBlockMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  public List<YcStaticBlockDto> findByBrandAnd5A(String brand) {
    return service.findByBrandAndEnabledAnd5A(brand).stream()
        .map(YcStaticBlockMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
