package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.ExternalLink;
import com.ladbrokescoral.oxygen.cms.api.service.ExternalLinkService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class ExternalLinks extends AbstractCrudController<ExternalLink> {

  @Autowired
  public ExternalLinks(ExternalLinkService crudService) {
    super(crudService);
  }

  @PostMapping("external-link")
  @Override
  public ResponseEntity create(@RequestBody @Validated ExternalLink entity) {
    return super.create(entity);
  }

  @GetMapping("external-link")
  @Override
  public List<ExternalLink> readAll() {
    return super.readAll();
  }

  @GetMapping("external-link/{id}")
  @Override
  public ExternalLink read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("external-link/{id}")
  @Override
  public ExternalLink update(@PathVariable String id, @RequestBody @Validated ExternalLink entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("external-link/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("external-link/brand/{brand}")
  @Override
  public List<ExternalLink> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }
}
