package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.FooterLogoService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class FooterLogos extends AbstractSortableController<FooterLogo> {

  private final FooterLogoService service;

  @Autowired
  FooterLogos(FooterLogoService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @PostMapping("footer-logo")
  @Override
  public ResponseEntity create(@RequestBody FooterLogo entity) {
    return super.create(entity);
  }

  @GetMapping("footer-logo")
  @Override
  public List<FooterLogo> readAll() {
    return super.readAll();
  }

  @GetMapping("footer-logo/{id}")
  @Override
  public FooterLogo read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("footer-logo/brand/{brand}")
  @Override
  public List<FooterLogo> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("footer-logo/{id}")
  @Override
  public FooterLogo update(@PathVariable String id, @RequestBody FooterLogo entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("footer-logo/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    FooterLogo footerLogo = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeImage(footerLogo);
    service.removeSvgImage(footerLogo);

    return delete(Optional.of(footerLogo));
  }

  @PostMapping("footer-logo/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("footer-logo/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<FooterLogo> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<FooterLogo> footerLogo = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      footerLogo = service.attachImage(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.SVG)) {
      footerLogo = service.attachSvgImage(maybeEntity.get(), file);
    }
    return footerLogo
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("footer-logo/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<FooterLogo> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<FooterLogo> removeResult = Optional.empty();
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
