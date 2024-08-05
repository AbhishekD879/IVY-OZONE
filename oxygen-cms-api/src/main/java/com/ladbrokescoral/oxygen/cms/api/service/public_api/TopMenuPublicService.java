package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TopMenuDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.TopMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.TopMenuService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class TopMenuPublicService {

  private final TopMenuService service;

  public TopMenuPublicService(TopMenuService service) {
    this.service = service;
  }

  public List<TopMenuDto> findByBrand(String brand) {
    return service.findAllByBrandAndDisabled(brand).stream()
        .map(TopMenuMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
