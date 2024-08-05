package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.HeaderContactMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.HeaderContactMenuRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HeaderContactMenuService extends AbstractMenuService<HeaderContactMenu> {

  private final HeaderContactMenuRepository headerContactMenuRepository;

  @Autowired
  public HeaderContactMenuService(HeaderContactMenuRepository repository) {
    super(repository);
    this.headerContactMenuRepository = repository;
  }

  public List<HeaderContactMenu> findAllPublic(String brand) {
    return headerContactMenuRepository.findAllByBrand(
        brand, SortableService.SORT_BY_SORT_ORDER_ASC);
  }
}
