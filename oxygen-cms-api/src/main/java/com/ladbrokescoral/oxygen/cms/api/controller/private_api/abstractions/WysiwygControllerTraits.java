package com.ladbrokescoral.oxygen.cms.api.controller.private_api.abstractions;

import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

/**
 * interface provides methods for both removing & adding wysiwyg images, whilst requires getters
 * of @{@link CrudService} descendants & @{@link WysiwygService} to be implemented.
 *
 * @param <T>
 */
public interface WysiwygControllerTraits<T> {

  CrudService<T> getCRUDService();

  WysiwygService getWysiwygService();

  default ResponseEntity uploadWysiwygImage(
      String brand, MultipartFile file, String collectionName, String id) {
    if (!getCRUDService().findOne(id).isPresent()) {
      throw new NotFoundException();
    }
    return getWysiwygService()
        .attachWyswigImage(brand, file, collectionName, id)
        .map(ResponseEntity::ok)
        .orElseGet(
            () -> new ResponseEntity("Failed to upload wysiwyg image.", HttpStatus.BAD_REQUEST));
  }

  default ResponseEntity removeWysiwygImage(
      String brand, String id, String collectionName, String imageName) {
    if (!getCRUDService().findOne(id).isPresent()) {
      throw new NotFoundException();
    }
    return getWysiwygService().removeWyswigImage(brand, collectionName, id, imageName)
        ? ResponseEntity.ok().build()
        : new ResponseEntity<>("Failed to remove wysiwyg image.", HttpStatus.BAD_REQUEST);
  }
}
