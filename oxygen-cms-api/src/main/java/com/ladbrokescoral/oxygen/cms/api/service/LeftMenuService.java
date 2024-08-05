package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.LeftMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.LeftMenuRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class LeftMenuService extends SortableService<LeftMenu> {

  private final LeftMenuRepository leftMenuRepository;

  @Autowired
  public LeftMenuService(LeftMenuRepository leftMenuRepository) {
    super(leftMenuRepository);
    this.leftMenuRepository = leftMenuRepository;
  }

  public List<LeftMenu> findAllByBrandSorted(String brand) {
    return leftMenuRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
