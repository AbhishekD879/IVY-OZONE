package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HRQuickLink;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.HRQuickLinkService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class HRQuickLinks extends AbstractSortableController<HRQuickLink> {

  private final HRQuickLinkService service;

  @Autowired
  HRQuickLinks(HRQuickLinkService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @PostMapping("hr-quick-link")
  @Override
  public ResponseEntity create(@RequestBody @Valid HRQuickLink entity) {
    return super.create(entity);
  }

  @GetMapping("hr-quick-link")
  @Override
  public List<HRQuickLink> readAll() {
    return super.readAll();
  }

  @GetMapping("hr-quick-link/{id}")
  @Override
  public HRQuickLink read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("hr-quick-link/brand/{brand}")
  @Override
  public List<HRQuickLink> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("hr-quick-link/{id}")
  @Override
  public HRQuickLink update(@PathVariable String id, @RequestBody @Valid HRQuickLink entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("hr-quick-link/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    HRQuickLink hrQuickLink = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeImage(hrQuickLink);

    return delete(Optional.of(hrQuickLink));
  }

  @PostMapping("hr-quick-link/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("hr-quick-link/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    Optional<HRQuickLink> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<HRQuickLink> hrQuickLink = service.attachImage(maybeEntity.get(), file);

    return hrQuickLink
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("hr-quick-link/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Optional<HRQuickLink> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    Optional<HRQuickLink> removeResult = service.removeImage(maybeEntity.get());

    return removeResult
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }
}
