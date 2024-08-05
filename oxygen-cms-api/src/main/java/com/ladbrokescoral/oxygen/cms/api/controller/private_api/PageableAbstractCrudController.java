package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.service.PageableCrudService;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

public abstract class PageableAbstractCrudController<T extends AbstractEntity>
    extends AbstractCrudController<T> {

  private PageableCrudService<T> pageableCrudService;

  PageableAbstractCrudController(PageableCrudService<T> pageableCrudService) {
    super(pageableCrudService);
    this.pageableCrudService = pageableCrudService;
  }

  public List<T> readAll(Optional<Integer> offset, Optional<Integer> limit) {
    if (offset.isPresent() && limit.isPresent()) {
      List<T> list = pageableCrudService.findAll(offset.get(), limit.get());
      Objects.requireNonNull(list);
      return list;
    }
    return super.readAll();
  }
}
