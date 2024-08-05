package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.UserMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.UserMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.UserMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.UserMenuService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class UserMenuPublicService {

  private final UserMenuService service;

  public UserMenuPublicService(UserMenuService service) {
    this.service = service;
  }

  public List<UserMenuDto> findByBrand(String brand) {
    List<UserMenu> userMenuCollection = service.findAllByBrandAndDisabled(brand);
    return userMenuCollection.stream()
        .map(UserMenuMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
