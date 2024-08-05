package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.HeaderSubMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.HeaderSubMenuRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HeaderSubMenuService extends AbstractMenuService<HeaderSubMenu> {

  private final HeaderSubMenuRepository headerSubMenuRepository;

  @Autowired
  public HeaderSubMenuService(HeaderSubMenuRepository headerSubMenuRepository) {
    super(headerSubMenuRepository);
    this.headerSubMenuRepository = headerSubMenuRepository;
  }

  public List<HeaderSubMenu> findAllByBrandAndDisabled(String brand) {
    return headerSubMenuRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(
        brand, Boolean.FALSE);
  }
}
