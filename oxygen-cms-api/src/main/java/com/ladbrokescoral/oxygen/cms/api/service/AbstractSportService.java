package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;

public abstract class AbstractSportService<T extends AbstractSportEntity>
    extends SortableService<T> {

  private EventHubService hubService;

  public AbstractSportService(CustomMongoRepository<T> repository, EventHubService hubService) {
    super(repository);
    this.hubService = hubService;
  }

  @Override
  public T prepareModelBeforeSave(T model) {
    if (PageType.eventhub.equals(model.getPageType())) {
      validateEventHub(model);
    }
    return super.prepareModelBeforeSave(model);
  }

  private void validateEventHub(T model) {
    Integer indexNumber = Integer.valueOf(model.getPageId());
    if (!hubService.existByBrandAndIndexNumber(model.getBrand(), indexNumber)) {
      throw new IllegalArgumentException(
          "Invalid eventHubId : " + model.getPageId() + " for brand : " + model.getBrand());
    }
  }
}
