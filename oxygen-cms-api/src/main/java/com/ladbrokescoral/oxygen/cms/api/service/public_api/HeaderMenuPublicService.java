package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.ChildMenusMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.HeaderMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderMenuService;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
public class HeaderMenuPublicService {

  private final HeaderMenuService service;

  public HeaderMenuPublicService(HeaderMenuService service) {
    this.service = service;
  }

  public List<HeaderMenuDto> findByBrand(String brand) {
    List<HeaderMenu> headerMenuCollection = service.findAllByBrandAndDisabled(brand);
    Map<String, List<HeaderMenu>> childMenusMap =
        ChildMenusMapper.extractChildMenus(headerMenuCollection.stream());
    return headerMenuCollection.stream()
        .filter(headerMenu -> StringUtils.isEmpty(headerMenu.getParent()))
        .map(
            headerMenu ->
                HeaderMenuMapper.INSTANCE.toDto(headerMenu, childMenusMap.get(headerMenu.getId())))
        .collect(Collectors.toList());
  }
}
