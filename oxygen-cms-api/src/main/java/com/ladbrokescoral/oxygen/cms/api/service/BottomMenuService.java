package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BottomMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.BottomMenuRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class BottomMenuService extends AbstractMenuService<BottomMenu> {

  private final BottomMenuRepository bottomMenuRepository;

  @Autowired
  public BottomMenuService(BottomMenuRepository repository) {
    super(repository);
    this.bottomMenuRepository = repository;
  }

  public List<BottomMenu> findAllPublic(String brand) {
    return bottomMenuRepository.findAllByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
  }
}
