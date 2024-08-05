package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Gallery;
import com.ladbrokescoral.oxygen.cms.api.service.GalleryService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class Galleries extends AbstractCrudController<Gallery> {
  @Autowired
  Galleries(GalleryService crudService) {
    super(crudService);
  }

  @PostMapping("gallery")
  @Override
  public ResponseEntity create(@RequestBody Gallery entity) {
    return super.create(entity);
  }

  @GetMapping("gallery")
  @Override
  public List<Gallery> readAll() {
    return super.readAll();
  }

  @GetMapping("gallery/{id}")
  @Override
  public Gallery read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("gallery/{id}")
  @Override
  public Gallery update(@PathVariable String id, @RequestBody Gallery entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("gallery/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
