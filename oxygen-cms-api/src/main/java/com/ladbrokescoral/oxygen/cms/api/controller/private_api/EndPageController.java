package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.EndPage;
import com.ladbrokescoral.oxygen.cms.api.service.EndPageService;
import java.util.List;
import javax.validation.Valid;
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
public class EndPageController extends AbstractCrudController<EndPage> {
  private final EndPageService service;

  EndPageController(EndPageService service) {
    super(service);
    this.service = service;
  }

  @PostMapping("/end-page")
  @Override
  public ResponseEntity create(@RequestBody @Valid EndPage entity) {
    return super.create(entity);
  }

  @GetMapping("/end-page")
  public List<EndPage> getAll() {
    return super.readAll();
  }

  @GetMapping("/end-page/{id}")
  public EndPage readById(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("/end-page/brand/{brand}")
  public List<EndPage> readEndPageByBrand(@PathVariable String brand) {
    return service.findByBrand(brand);
  }

  @PutMapping("/end-page/{id}")
  @Override
  public EndPage update(@PathVariable String id, @RequestBody @Valid EndPage entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("/end-page/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("/end-page/{id}/background")
  public EndPage uploadImage(
      @PathVariable String id, @RequestParam(value = "background") MultipartFile background) {
    return service.uploadBackground(id, background);
  }

  @DeleteMapping("/end-page/{id}/background")
  public void deleteImage(@PathVariable String id) {
    service.deleteBackground(id);
  }
}
