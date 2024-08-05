package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.RightMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.RightMenuService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class RightMenuPublicService {

  private final RightMenuService service;

  public RightMenuPublicService(RightMenuService service) {
    this.service = service;
  }

  public List<RightMenuDto> findByBrand(String brand) {

    brand = Util.updateBrand(brand);

    List<RightMenu> rightMenuCollection = service.findAllByBrand(brand);
    return rightMenuCollection.stream()
        .map(RightMenuMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
