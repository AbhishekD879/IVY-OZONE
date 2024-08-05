package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class SportModules extends AbstractSortableController<SportModule> {

  private SportModuleService service;

  @Autowired
  public SportModules(SportModuleService service) {
    super(service);
    this.service = service;
  }

  @PostMapping("sport-module")
  @Override
  public ResponseEntity create(@Valid @RequestBody SportModule entity) {

    return super.create(entity);
  }

  @GetMapping("sport-module")
  @Override
  public List<SportModule> readAll() {
    return super.readAll();
  }

  @GetMapping("sport-module/{id}")
  @Override
  public SportModule read(@PathVariable String id) {
    return super.read(id);
  }

  @DeleteMapping("sport-module/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("sport-module/brand/{brand}")
  @Override
  public List<SportModule> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("sport-module/brand/{brand}/{pageType}/{sportId}")
  public List<SportModule> readByBrandAndSportId(
      @PathVariable String brand, @PathVariable PageType pageType, @PathVariable String sportId) {
    return service.findAll(brand, pageType, sportId);
  }

  @PutMapping("sport-module/{id}")
  @Override
  public SportModule update(@PathVariable String id, @Valid @RequestBody SportModule entity) {
    return super.update(id, entity);
  }

  @PostMapping("sport-module/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
