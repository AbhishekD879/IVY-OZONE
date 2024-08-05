package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController.notFound;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.StructurePublicService;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SystemConfigurationApi implements Public {

  private final StructurePublicService service;

  @Autowired
  public SystemConfigurationApi(StructurePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/system-configuration")
  public ResponseEntity<Map<String, Map<String, Object>>> findByBrand(
      @PathVariable("brand") String brand) {
    return service.find(brand).map(ResponseEntity::ok).orElseGet(notFound());
  }

  @GetMapping(value = "{brand}/system-configurations/{name}")
  public ResponseEntity<Map<String, Object>> findElementByBrand(
      @PathVariable("brand") String brand, @PathVariable("name") String configName) {
    return service.findElement(brand, configName).map(ResponseEntity::ok).orElseGet(notFound());
  }
}
