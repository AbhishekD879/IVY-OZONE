package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.RenderConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RenderConfig;
import com.ladbrokescoral.oxygen.cms.api.mapping.RenderConfigMapper;
import com.ladbrokescoral.oxygen.cms.api.service.RenderConfigService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class RenderConfigPublicService {

  private final RenderConfigService service;

  public RenderConfigPublicService(RenderConfigService service) {
    this.service = service;
  }

  public List<RenderConfigDto> findByBrand(String brand) {
    List<RenderConfig> config = service.findByBrand(brand);
    return config.stream().map(RenderConfigMapper.INSTANCE::toDto).collect(Collectors.toList());
  }
}
