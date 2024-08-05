package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.HeaderMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.HeaderMenuRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HeaderMenuService extends AbstractMenuService<HeaderMenu> {

  private final HeaderMenuRepository headerMenuRepository;

  @Autowired
  public HeaderMenuService(HeaderMenuRepository headerMenuRepository) {
    super(headerMenuRepository);
    this.headerMenuRepository = headerMenuRepository;
  }

  public List<HeaderMenu> findAllByBrandAndDisabled(String brand) {
    return headerMenuRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
  }
}
