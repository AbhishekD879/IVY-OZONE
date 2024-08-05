package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;

public abstract class AbstractSortableController<T extends SortableEntity>
    extends AbstractCrudController<T> {

  protected final SortableService<T> sortableService;

  AbstractSortableController(SortableService<T> sortableService) {
    super(sortableService);
    this.sortableService = sortableService;
  }

  public void order(OrderDto newOrder) {
    sortableService.dragAndDropOrder(newOrder);
  }
}
