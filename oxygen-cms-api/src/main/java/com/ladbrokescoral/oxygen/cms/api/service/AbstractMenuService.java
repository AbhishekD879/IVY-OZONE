package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractMenuEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;

@Slf4j
@Validated
public class AbstractMenuService<T extends AbstractMenuEntity> extends SortableService<T> {

  CustomMongoRepository<T> pagingAndSortingRepository;

  public AbstractMenuService(CustomMongoRepository<T> pagingAndSortingRepository) {
    super(pagingAndSortingRepository);
    this.pagingAndSortingRepository = pagingAndSortingRepository;
  }

  @Override
  public T prepareModelBeforeSave(T model) {
    model.setLinkTitleBrand(generateLinkTitleBrand(model));
    return model;
  }

  private String generateLinkTitleBrand(T model) {
    return new StringBuilder(model.getLinkTitle())
        .append("-")
        .append(model.getBrand())
        .toString()
        .toLowerCase();
  }
}
