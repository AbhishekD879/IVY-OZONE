package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.*;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.FooterMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.FooterMenuService;
import java.util.Collection;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class FooterMenuPublicService {

  private final FooterMenuService service;

  public FooterMenuPublicService(FooterMenuService service) {
    this.service = service;
  }

  public List<FooterMenuV3Dto> find(String brand) {
    List<FooterMenu> footerMenuCollection = service.findAllByBrandAndDisabled(brand);
    return reduceCollection(footerMenuCollection).getFooterMenus().stream()
        .map(FooterMenuMapper.INSTANCE::toDtoV3)
        .collect(Collectors.toList());
  }

  private FooterMenuIntermediateContainerDto reduceCollection(Collection<FooterMenu> collection) {
    FooterMenuIntermediateContainerDto container = new FooterMenuIntermediateContainerDto();
    for (FooterMenu fMenu : collection) {
      configureFooterMenuContainer(container, fMenu);
    }

    return container;
  }

  private void configureFooterMenuContainer(
      FooterMenuIntermediateContainerDto container, FooterMenu fMenu) {
    if ((container.getMobile() < 5 && fMenu.isMobile())
        || (container.getTablet() < 5 && fMenu.isTablet())
        || (container.getDesktop() < 5 && fMenu.isDesktop())) {

      container.getFooterMenus().add(fMenu);
      if (fMenu.isMobile()) {
        container.setMobile(container.getMobile() + 1);
      }
      if (fMenu.isTablet()) {
        container.setTablet(container.getTablet() + 1);
      }
      if (fMenu.isDesktop()) {
        container.setDesktop(container.getDesktop() + 1);
      }
    }
  }

  public List<FooterMenuV2Dto> find(String brand, String deviceType) {
    return find(brand, deviceType, SegmentConstants.UNIVERSAL, FooterMenuMapper.INSTANCE::toDtoV2);
  }

  public List<InitialDataFooterMenuV2Dto> findInitialData(
      String brand, String deviceType, String segmentName) {
    return find(brand, deviceType, segmentName, FooterMenuMapper.INSTANCE::toInitialDtoV2);
  }

  public <T> List<T> find(
      String brand, String deviceType, String segmentName, Function<FooterMenu, T> dtoMapper) {
    Collection<FooterMenu> menus =
        service.findAllByBrandAndDeviceType(brand, deviceType, segmentName);
    return menus.stream().map(dtoMapper).collect(Collectors.toList());
  }

  public List<FooterMenuSegmentedDto> findAllActiveByBrand(String brand) {
    return service.findAllActiveByBrand(brand);
  }
}
