package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.FooterMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.SegmentNamePattern;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@Validated
public class FooterMenus extends AbstractSortableController<FooterMenu> {

  private final FooterMenuService service;

  @Autowired
  FooterMenus(FooterMenuService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @PostMapping("footer-menu")
  @Override
  public ResponseEntity create(@RequestBody @Validated FooterMenu entity) {
    return super.create(entity);
  }

  @GetMapping("footer-menu")
  @Override
  public List<FooterMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("footer-menu/{id}")
  @Override
  public FooterMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("footer-menu/brand/{brand}")
  @Override
  public List<FooterMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("footer-menu/brand/{brand}/segment/{segmentName}")
  public List<FooterMenu> readByBrandAndSegment(
      @PathVariable @Brand String brand, @PathVariable @SegmentNamePattern String segmentName) {
    return service.findByBrandAndSegmentName(brand, segmentName);
  }

  @PutMapping("footer-menu/{id}")
  @Override
  public FooterMenu update(@PathVariable String id, @RequestBody @Validated FooterMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("footer-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    FooterMenu menu = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeImage(menu);
    service.removeSvgImage(menu);

    return delete(Optional.of(menu));
  }

  @PostMapping("footer-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("footer-menu/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<FooterMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<FooterMenu> footerMenu = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      footerMenu = service.attachImage(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.SVG)) {
      footerMenu = service.attachSvgImage(maybeEntity.get(), file);
    }

    return footerMenu
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("footer-menu/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<FooterMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<FooterMenu> removeResult = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      removeResult = service.removeImage(maybeEntity.get());
    }
    if (fileType.equals(FileType.SVG)) {
      removeResult = service.removeSvgImage(maybeEntity.get());
    }

    return removeResult
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }
}
