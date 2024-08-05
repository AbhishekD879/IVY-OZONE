package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SsoPageDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SsoPageMapper;
import com.ladbrokescoral.oxygen.cms.api.service.SsoPageService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class SsoPagePublicService {

  private final SsoPageService service;

  public SsoPagePublicService(SsoPageService service) {
    this.service = service;
  }

  public List<SsoPageDto> findByBrand(String brand, String osType) {
    return service.findSsoPages(brand, osType).stream()
        .map(value -> SsoPageMapper.INSTANCE.toDto(value, osType))
        .collect(Collectors.toList());
  }
}
