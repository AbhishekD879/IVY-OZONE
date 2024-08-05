package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderContactMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderContactMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.HeaderContactMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderContactMenuService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class HeaderContactMenuPublicService {

  private final HeaderContactMenuService service;

  public HeaderContactMenuPublicService(HeaderContactMenuService service) {
    this.service = service;
  }

  public List<HeaderContactMenuDto> find(String brand) {
    List<HeaderContactMenu> headerContactMenus = service.findAllPublic(brand);
    return headerContactMenus.stream()
        .map(HeaderContactMenuMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
