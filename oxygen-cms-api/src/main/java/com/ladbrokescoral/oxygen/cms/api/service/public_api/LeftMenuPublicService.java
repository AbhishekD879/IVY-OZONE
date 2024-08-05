package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LeftMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LeftMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.ChildMenusMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.DtoMapper;
import com.ladbrokescoral.oxygen.cms.api.service.LeftMenuService;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
public class LeftMenuPublicService {

  private final LeftMenuService service;

  public LeftMenuPublicService(LeftMenuService service) {
    this.service = service;
  }

  public List<LeftMenuDto> findByBrand(String brand) {
    List<LeftMenu> leftMenuCollection = service.findAllByBrandSorted(brand);
    Map<String, List<LeftMenu>> childMenusMap =
        ChildMenusMapper.extractChildMenus(leftMenuCollection.stream());
    return leftMenuCollection.stream()
        .filter(leftMenu -> StringUtils.isEmpty(leftMenu.getParent()))
        .map(leftMenu -> DtoMapper.toDto(leftMenu, childMenusMap.get(leftMenu.getId())))
        .collect(Collectors.toList());
  }
}
