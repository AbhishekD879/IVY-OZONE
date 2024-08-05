package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.RenderConfig;
import com.ladbrokescoral.oxygen.cms.api.service.RenderConfigService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class RenderConfigs extends AbstractCrudController<RenderConfig> {

  private final RenderConfigService service;

  @Autowired
  RenderConfigs(RenderConfigService service) {
    super(service);
    this.service = service;
  }

  @PostMapping("render-config")
  @Override
  public ResponseEntity create(@RequestBody @Validated RenderConfig entity) {
    service.validate(entity);
    entity.setDevice(entity.getDevice().toUpperCase());
    return super.create(entity);
  }

  @GetMapping("render-config")
  @Override
  public List<RenderConfig> readAll() {
    return super.readAll();
  }

  @GetMapping("render-config/{id}")
  @Override
  public RenderConfig read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("render-config/brand/{brand}")
  @Override
  public List<RenderConfig> readByBrand(@PathVariable String brand) {
    List<RenderConfig> renderConfig = service.findByBrand(brand);
    return super.populateCreatorAndUpdater(renderConfig);
  }

  @PutMapping("render-config/{id}")
  @Override
  public RenderConfig update(@PathVariable String id, @RequestBody @Validated RenderConfig entity) {
    service.validate(entity);
    entity.setDevice(entity.getDevice().toUpperCase());
    return super.update(id, entity);
  }

  @DeleteMapping("render-config/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
