package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.OtfIosAppToggle;
import com.ladbrokescoral.oxygen.cms.api.service.OtfIosAppToggleService;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OtfIosAppToggles extends AbstractCrudController<OtfIosAppToggle> {
  private final OtfIosAppToggleService service;

  OtfIosAppToggles(OtfIosAppToggleService service) {
    super(service);
    this.service = service;
  }

  @Override
  @PostMapping("/otf-ios-app-toggle")
  public ResponseEntity<OtfIosAppToggle> create(@RequestBody @Valid OtfIosAppToggle entity) {
    return super.create(entity);
  }

  @Override
  @PutMapping("/otf-ios-app-toggle/{id}")
  public OtfIosAppToggle update(
      @PathVariable String id, @RequestBody @Valid OtfIosAppToggle entity) {
    return super.update(id, entity);
  }

  @GetMapping("/otf-ios-app-toggle/brand/{brand}")
  public OtfIosAppToggle readOneByBrand(@PathVariable String brand) {
    return service.findOneByBrand(brand);
  }
}
