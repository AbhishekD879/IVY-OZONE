package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ConnectMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.ChildMenusMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.ConnectMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.ConnectMenuService;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
public class ConnectMenuPublicService implements ApiService<ConnectMenuDto> {

  private final ConnectMenuService service;

  public ConnectMenuPublicService(ConnectMenuService service) {
    this.service = service;
  }

  public List<ConnectMenuDto> findByBrand(String brand) {

    List<ConnectMenu> connectMenuCollection = service.findAllByBrandAndDisabled(brand);

    Map<String, List<ConnectMenu>> childMenusMap =
        ChildMenusMapper.extractChildMenus(connectMenuCollection.stream());

    return connectMenuCollection.stream()
        .filter(connectMenu -> StringUtils.isEmpty(connectMenu.getParent()))
        .map(
            connectMenu ->
                ConnectMenuMapper.INSTANCE.toDto(
                    connectMenu, childMenusMap.get(connectMenu.getId())))
        .collect(Collectors.toList());
  }
}
