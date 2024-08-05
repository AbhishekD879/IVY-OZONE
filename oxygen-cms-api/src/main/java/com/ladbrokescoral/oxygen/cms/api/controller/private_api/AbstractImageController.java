package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.service.ImageOperationsService;
import java.util.Optional;
import org.springframework.http.ResponseEntity;

// TODO move image upload/remove logic here

/**
 * this controller provides generic method(s) for image delete related logic.
 *
 * @param <T>
 */
public abstract class AbstractImageController<T extends SortableEntity>
    extends AbstractSortableController<T> {

  private final ImageOperationsService<T> imageOperationsService;

  AbstractImageController(ImageOperationsService<T> imageOperationsService) {
    super(imageOperationsService);
    this.imageOperationsService = imageOperationsService;
  }

  /**
   * remove all images related to object, and then object itself.
   *
   * @param id
   * @return
   */
  @Override
  public ResponseEntity delete(String id) {
    return imageOperationsService
        .findOne(id)
        .map(
            (T banner) -> {
              imageOperationsService.removeImages(banner);
              return delete(Optional.of(banner));
            })
        .orElseGet(notFound());
  }
}
