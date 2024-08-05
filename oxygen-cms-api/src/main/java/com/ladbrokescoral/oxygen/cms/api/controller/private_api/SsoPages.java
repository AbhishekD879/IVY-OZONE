package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.SsoPageService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class SsoPages extends AbstractImageController<SsoPage> {

  private SsoPageService ssoPageService;

  @Autowired
  SsoPages(SsoPageService crudService) {
    super(crudService);
    ssoPageService = crudService;
  }

  @GetMapping("sso-page")
  @Override
  public List<SsoPage> readAll() {
    return super.readAll();
  }

  @GetMapping("sso-page/{id}")
  @Override
  public SsoPage read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("sso-page/brand/{brand}")
  @Override
  public List<SsoPage> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("sso-page")
  @Override
  public ResponseEntity create(@RequestBody @Validated SsoPage entity) {
    return super.create(entity);
  }

  @PutMapping("sso-page/{id}")
  @Override
  public SsoPage update(@PathVariable String id, @RequestBody @Validated SsoPage entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("sso-page/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("sso-page/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("sso-page/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    Optional<SsoPage> maybeEntity = ssoPageService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    Optional<SsoPage> offerOptional = ssoPageService.attachImage(maybeEntity.get(), file);
    return offerOptional
        .map(
            ssoPage -> {
              SsoPage saved = ssoPageService.save(ssoPage);
              return new ResponseEntity(saved, HttpStatus.OK);
            })
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("sso-page/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    SsoPage ssoPage = ssoPageService.findOne(id).orElseThrow(NotFoundException::new);

    return ssoPageService
        .removeImages(ssoPage)
        .map(ssoPageService::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }
}
