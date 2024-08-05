package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class ModuleRibbonTabs extends AbstractSortableController<ModuleRibbonTab> {

  ModuleRibbonTabService moduleRibbonTabService;

  @Autowired
  ModuleRibbonTabs(ModuleRibbonTabService moduleRibbonTabService) {
    super(moduleRibbonTabService);
    this.moduleRibbonTabService = moduleRibbonTabService;
  }

  @PostMapping("module-ribbon-tab")
  @Override
  public ResponseEntity create(@Validated @RequestBody ModuleRibbonTab moduleRibbonTab) {
    return super.create(moduleRibbonTab);
  }

  @GetMapping("module-ribbon-tab")
  @Override
  public List<ModuleRibbonTab> readAll() {
    return super.readAll();
  }

  @GetMapping("module-ribbon-tab/{id}")
  @Override
  public ModuleRibbonTab read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("module-ribbon-tab/brand/{brand}")
  @Override
  public List<ModuleRibbonTab> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("module-ribbon-tab/{id}")
  @Override
  public ModuleRibbonTab update(
      @PathVariable String id, @RequestBody @Validated ModuleRibbonTab entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("module-ribbon-tab/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("module-ribbon-tab/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @GetMapping("module-ribbon-tab/brand/{brand}/segment/{segmentName}")
  public List<ModuleRibbonTab> readByBrandAndSegmentName(
      @PathVariable String brand, @PathVariable String segmentName) {
    return moduleRibbonTabService.findByBrandAndSegmentName(brand, segmentName);
  }
}
