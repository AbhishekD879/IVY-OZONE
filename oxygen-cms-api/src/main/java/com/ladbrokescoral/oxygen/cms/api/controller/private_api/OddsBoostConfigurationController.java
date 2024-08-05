package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostConfigEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.service.OddsBoostConfigurationService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@Validated
public class OddsBoostConfigurationController
    extends AbstractCrudController<OddsBoostConfigEntity> {

  private final OddsBoostConfigurationService service;

  public OddsBoostConfigurationController(final OddsBoostConfigurationService service) {
    super(service);
    this.service = service;
  }

  @PostMapping("odds-boost")
  @Override
  public ResponseEntity<OddsBoostConfigEntity> create(
      @RequestBody @Validated OddsBoostConfigEntity entity) {
    entity.setId(entity.getBrand().toLowerCase());
    return super.createWithId(entity);
  }

  @GetMapping("odds-boost/{id}")
  @Override
  public OddsBoostConfigEntity read(@PathVariable String id) {
    return service
        .findOne(id.toLowerCase())
        .map(this::populateCreatorAndUpdater)
        .orElseGet(() -> defaultEntity(id));
  }

  private OddsBoostConfigEntity defaultEntity(String id) {
    OddsBoostConfigEntity entity = new OddsBoostConfigEntity();
    entity.setBrand(id.toLowerCase());
    return entity;
  }

  @PutMapping("odds-boost/{id}")
  @Override
  public OddsBoostConfigEntity update(
      @PathVariable String id, @RequestBody @Validated OddsBoostConfigEntity updateEntity) {
    if (updateEntity.getBrand().equalsIgnoreCase(id)) {
      return super.forceUpdate(id, updateEntity);
    }
    throw new ValidationException("Can't validate entity. Id should be equals to brand name");
  }

  @DeleteMapping("odds-boost/{id}")
  @Override
  public ResponseEntity<OddsBoostConfigEntity> delete(@PathVariable String id) {
    return super.delete(id.toLowerCase());
  }

  @PostMapping("odds-boost/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "svg", required = false) FileType fileType) {
    if (!fileType.equals(FileType.SVG)) {
      return new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST);
    }
    OddsBoostConfigEntity entity = service.findOne(id).orElseThrow(NotFoundException::new);
    return service
        .attachSvgImage(entity, file)
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("odds-boost/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "svg", required = false) FileType fileType) {
    if (!fileType.equals(FileType.SVG)) {
      return new ResponseEntity<>("Failed to remove image", HttpStatus.BAD_REQUEST);
    }
    OddsBoostConfigEntity entity = service.findOne(id).orElseThrow(NotFoundException::new);
    return service
        .removeSvgImage(entity)
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }
}
