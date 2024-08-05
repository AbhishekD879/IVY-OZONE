package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.OtfGameTabs;
import com.ladbrokescoral.oxygen.cms.api.service.OtfGameTabsService;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@SuppressWarnings("java:S4684")
public class OtfGameTabsController extends AbstractCrudController<OtfGameTabs> {
  private final OtfGameTabsService otfGameTabsService;

  protected OtfGameTabsController(OtfGameTabsService otfGameTabsService) {
    super(otfGameTabsService);
    this.otfGameTabsService = otfGameTabsService;
  }

  @PostMapping("/otf-tab-config")
  @Override
  public ResponseEntity<OtfGameTabs> create(@RequestBody @Valid OtfGameTabs otfGameTabs) {
    return super.create(otfGameTabs);
  }

  @PutMapping("/otf-tab-config/{id}")
  @Override
  public OtfGameTabs update(@PathVariable String id, @RequestBody @Valid OtfGameTabs otfGameTabs) {
    return super.update(id, otfGameTabs);
  }

  @GetMapping("/otf-tab-config/brand/{brand}")
  public OtfGameTabs findByBrand(@PathVariable String brand) {
    return otfGameTabsService.findByBrand(brand).stream().findFirst().orElseGet(OtfGameTabs::new);
  }

  @DeleteMapping("/otf-tab-config/{id}")
  @Override
  public ResponseEntity<OtfGameTabs> delete(@PathVariable String id) {
    return super.delete(id);
  }
}
