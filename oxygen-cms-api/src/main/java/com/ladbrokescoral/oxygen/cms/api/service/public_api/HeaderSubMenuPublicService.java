package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderSubMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderSubMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.HeaderSubMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderSubMenuService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class HeaderSubMenuPublicService {

  private final HeaderSubMenuService service;

  public HeaderSubMenuPublicService(HeaderSubMenuService service) {
    this.service = service;
  }

  public List<HeaderSubMenuDto> findByBrand(String brand) {
    List<HeaderSubMenu> headerSubMenuCollection = service.findAllByBrandAndDisabled(brand);
    return headerSubMenuCollection.stream()
        .map(HeaderSubMenuMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
