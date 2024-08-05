package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.MaintenancePageService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class MaintenancePages extends AbstractImageController<MaintenancePage> {

  private final MaintenancePageService maintenancePageService;

  @Autowired
  MaintenancePages(MaintenancePageService maintenancePageService) {
    super(maintenancePageService);
    this.maintenancePageService = maintenancePageService;
  }

  @PostMapping("maintenance-page")
  @Override
  public ResponseEntity create(@RequestBody @Valid MaintenancePage entity) {
    return super.create(entity);
  }

  @GetMapping("maintenance-page")
  @Override
  public List<MaintenancePage> readAll() {
    return super.readAll();
  }

  @GetMapping("maintenance-page/{id}")
  @Override
  public MaintenancePage read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("maintenance-page/brand/{brand}")
  @Override
  public List<MaintenancePage> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("maintenance-page/{id}")
  @Override
  public MaintenancePage update(
      @PathVariable String id, @RequestBody @Valid MaintenancePage entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("maintenance-page/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("maintenance-page/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {

    Optional<MaintenancePage> entity = maintenancePageService.findOne(id);
    if (!entity.isPresent()) {
      return new ResponseEntity(HttpStatus.NOT_FOUND);
    }

    Optional<MaintenancePage> maintenancePage =
        maintenancePageService.uploadImage(entity.get(), file);

    return maintenancePage
        .map(mp -> new ResponseEntity(maintenancePageService.save(mp), HttpStatus.OK))
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("maintenance-page/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    MaintenancePage maintenancePage =
        maintenancePageService.findOne(id).orElseThrow(NotFoundException::new);

    return maintenancePageService
        .removeImages(maintenancePage)
        .map(maintenancePageService::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }
}
