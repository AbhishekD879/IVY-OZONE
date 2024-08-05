package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DesktopQuickLink;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.DesktopQuickLinkService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class DesktopQuickLinks extends AbstractSortableController<DesktopQuickLink> {

  private final DesktopQuickLinkService service;

  @Autowired
  DesktopQuickLinks(DesktopQuickLinkService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @PostMapping("desktop-quick-link")
  @Override
  public ResponseEntity create(@RequestBody DesktopQuickLink entity) {
    return super.create(entity);
  }

  @GetMapping("desktop-quick-link")
  @Override
  public List<DesktopQuickLink> readAll() {
    return super.readAll();
  }

  @GetMapping("desktop-quick-link/{id}")
  @Override
  public DesktopQuickLink read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("desktop-quick-link/brand/{brand}")
  @Override
  public List<DesktopQuickLink> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("desktop-quick-link/{id}")
  @Override
  public DesktopQuickLink update(@PathVariable String id, @RequestBody DesktopQuickLink entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("desktop-quick-link/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    DesktopQuickLink lnQuickLink = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeImage(lnQuickLink);

    return delete(Optional.of(lnQuickLink));
  }

  @PostMapping("desktop-quick-link/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("desktop-quick-link/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    Optional<DesktopQuickLink> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<DesktopQuickLink> lnQuickLink = service.attachImage(maybeEntity.get(), file);

    return lnQuickLink
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("desktop-quick-link/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Optional<DesktopQuickLink> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    Optional<DesktopQuickLink> removeResult = service.removeImage(maybeEntity.get());

    return removeResult
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }
}
