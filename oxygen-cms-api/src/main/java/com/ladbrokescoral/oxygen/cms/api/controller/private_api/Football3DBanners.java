package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Football3DBanner;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.Football3DBannerService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class Football3DBanners extends AbstractImageController<Football3DBanner> {
  private final Football3DBannerService service;

  @Autowired
  Football3DBanners(Football3DBannerService crudService) {
    super(crudService);
    service = crudService;
  }

  @PostMapping("football-3d-banner")
  @Override
  public ResponseEntity create(@RequestBody @Valid Football3DBanner entity) {
    return super.create(entity);
  }

  @GetMapping("football-3d-banner")
  @Override
  public List<Football3DBanner> readAll() {
    return super.readAll();
  }

  @GetMapping("football-3d-banner/{id}")
  @Override
  public Football3DBanner read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("football-3d-banner/brand/{brand}")
  @Override
  public List<Football3DBanner> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("football-3d-banner/{id}")
  @Override
  public Football3DBanner update(
      @PathVariable String id, @RequestBody @Valid Football3DBanner entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("football-3d-banner/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("football-3d-banner/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    return service
        .findOne(id)
        .map(dBanner -> service.uploadImage(dBanner, file).get())
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @DeleteMapping("football-3d-banner/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Football3DBanner football3DBanner = service.findOne(id).orElseThrow(NotFoundException::new);

    return service
        .removeImages(football3DBanner)
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }

  @PostMapping("football-3d-banner/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
