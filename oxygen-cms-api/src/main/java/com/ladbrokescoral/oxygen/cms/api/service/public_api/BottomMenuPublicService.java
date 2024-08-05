package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BottomMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BottomMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.BottomMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.BottomMenuService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class BottomMenuPublicService implements ApiService<BottomMenuDto> {

  private final BottomMenuService service;

  public BottomMenuPublicService(BottomMenuService service) {
    this.service = service;
  }

  public List<BottomMenuDto> findByBrand(String brand) {
    List<BottomMenu> bottomMenus = service.findAllPublic(brand);
    return bottomMenus.stream().map(BottomMenuMapper.INSTANCE::toDto).collect(Collectors.toList());
  }
}
