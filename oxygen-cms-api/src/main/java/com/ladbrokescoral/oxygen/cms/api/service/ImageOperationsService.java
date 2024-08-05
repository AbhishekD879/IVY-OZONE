package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import java.util.Optional;

public abstract class ImageOperationsService<T extends SortableEntity> extends SortableService<T> {

  public ImageOperationsService(CustomMongoRepository<T> repository) {
    super(repository);
  }

  public abstract Optional<T> removeImages(T entity);
}
