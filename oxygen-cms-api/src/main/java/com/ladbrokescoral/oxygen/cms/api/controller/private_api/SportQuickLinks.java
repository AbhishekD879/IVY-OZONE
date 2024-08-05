package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.SportQuickLinkService;
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
public class SportQuickLinks extends AbstractSortableController<SportQuickLink> {

  private SportQuickLinkService service;

  @Autowired
  public SportQuickLinks(SportQuickLinkService service) {
    super(service);
    this.service = service;
  }

  @PostMapping("sport-quick-link")
  @Override
  public ResponseEntity create(@Valid @RequestBody SportQuickLink entity) {
    return super.create(entity);
  }

  @GetMapping("sport-quick-link")
  @Override
  public List<SportQuickLink> readAll() {
    return super.readAll();
  }

  @GetMapping("sport-quick-link/{id}")
  @Override
  public SportQuickLink read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("sport-quick-link/brand/{brand}")
  @Override
  public List<SportQuickLink> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("sport-quick-link/brand/{brand}/{pageType}/{pageId}")
  public List<SportQuickLink> readByBrand(
      @PathVariable String brand,
      @PathVariable @Valid PageType pageType,
      @PathVariable String pageId) {
    return service.findAllByBrandAndPageTypeAndPageId(brand, pageType, pageId);
  }

  @PutMapping("sport-quick-link/{id}")
  @Override
  public SportQuickLink update(@PathVariable String id, @Valid @RequestBody SportQuickLink entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("sport-quick-link/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    SportQuickLink quickLink = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeSvgImage(quickLink);
    return delete(Optional.of(quickLink));
  }

  @PostMapping("sport-quick-link/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("sport-quick-link/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    Optional<SportQuickLink> sportQuickLink = service.findOne(id);
    if (!sportQuickLink.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    sportQuickLink = service.attachSvgImage(sportQuickLink.get(), file);
    return sportQuickLink
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("sport-quick-link/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Optional<SportQuickLink> quickLink = service.findOne(id);
    if (!quickLink.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    Optional<SportQuickLink> removeResult = service.removeSvgImage(quickLink.get());
    return removeResult
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }

  @GetMapping("sport-quick-link/brand/{brand}/segment/{segmentName}")
  public List<SportQuickLink> readByBrandAndSegmentName(
      @PathVariable String brand, @PathVariable String segmentName) {
    return service.findByBrandAndSegmentName(brand, segmentName);
  }

  @GetMapping("sport-quick-link/brand/{brand}/segment/{segmentName}/{pageType}/{pageId}")
  public List<SportQuickLink> readByBrandAndSegmentName(
      @PathVariable String brand,
      @PathVariable String segmentName,
      @PathVariable @Valid String pageType,
      @PathVariable String pageId) {
    return service.findByBrandAndSegmentNameAndPageRef(brand, pageType, pageId, segmentName);
  }
}
