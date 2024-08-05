package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TopMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.TopMenuRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class TopMenuService extends SortableService<TopMenu> {

  private final TopMenuRepository topMenuRepository;

  @Autowired
  public TopMenuService(TopMenuRepository topMenuRepository) {
    super(topMenuRepository);
    this.topMenuRepository = topMenuRepository;
  }

  public List<TopMenu> findAllByBrandAndDisabled(String brand) {
    return topMenuRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, false);
  }
}
