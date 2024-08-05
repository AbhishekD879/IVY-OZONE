package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import com.ladbrokescoral.oxygen.cms.api.service.BannerService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.BannerImageService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class Banners extends AbstractSortableController<Banner> {

  private final BannerService service;
  private final BannerImageService bannerImageService;

  @Autowired
  public Banners(final BannerService service, final BannerImageService bannerService) {
    super(service);
    this.service = service;
    this.bannerImageService = bannerService;
  }

  @PostMapping(value = "banner")
  @Override
  public ResponseEntity create(@RequestBody @Valid Banner entity) {
    return super.create(entity);
  }

  @JsonView(Views.GetAll.class)
  @GetMapping(value = "banner")
  @Override
  public List<Banner> readAll() {
    return super.readAll();
  }

  @GetMapping("banner/{id}")
  @Override
  public Banner read(@PathVariable String id) {
    return super.read(id);
  }

  @JsonView(Views.GetAll.class)
  @GetMapping("banner/brand/{brand}")
  @Override
  public List<Banner> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping(value = "banner/{id}")
  @Override
  public Banner update(@PathVariable String id, @RequestBody @Valid Banner entity) {
    return super.update(id, entity);
  }

  @DeleteMapping(value = "banner/{id}")
  @Override
  public ResponseEntity delete(@PathVariable("id") String id) {
    Optional<Banner> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    bannerImageService.removeMediumAndSmallImages(maybeEntity.get());
    bannerImageService.removeDesktopImage(maybeEntity.get());
    service.delete(id);
    return new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }

  @PostMapping("/banner/uploadImage/{bannerId}")
  public ResponseEntity handleFileUpload(
      @PathVariable("bannerId") String bannerId,
      @RequestParam(value = "desktopImage", required = false, defaultValue = "false")
          boolean isDesktopImage,
      @RequestParam("file") MultipartFile file) {
    Optional<Banner> maybeEntity = service.findOne(bannerId);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<Banner> banner =
        isDesktopImage
            ? bannerImageService.updateDesktopImage(maybeEntity.get(), file)
            : bannerImageService.updateMediumAndSmallImages(maybeEntity.get(), file);

    return banner.map(service::save).map(ResponseEntity::ok).orElseGet(failedToUpdateImage());
  }

  @DeleteMapping("banner/removeImage/{bannerId}")
  public ResponseEntity handleFileRemove(
      @PathVariable("bannerId") String bannerId,
      @RequestParam(value = "desktopImage", required = false, defaultValue = "false")
          boolean isDesktopImage) {
    Optional<Banner> maybeEntity = service.findOne(bannerId);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    return (isDesktopImage
            ? bannerImageService.removeDesktopImage(maybeEntity.get())
            : bannerImageService.removeMediumAndSmallImages(maybeEntity.get()))
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }

  @PostMapping("banner/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
