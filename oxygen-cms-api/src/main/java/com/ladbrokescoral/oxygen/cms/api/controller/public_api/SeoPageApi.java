package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController.notFound;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeoPagePublicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SeoPageApi implements Public {

  private final SeoPagePublicService service;

  @Autowired
  public SeoPageApi(SeoPagePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/seo-pages")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    return new ResponseEntity<>(service.find(brand), HttpStatus.OK);
  }

  @GetMapping(value = "{brand}/seo-page/{id}")
  public ResponseEntity findByBrand(
      @PathVariable("brand") String brand, @PathVariable("id") String id) {
    return service
        .find(brand, id)
        .map(seoPageDto -> new ResponseEntity<>(seoPageDto, HttpStatus.OK))
        .orElseGet(notFound());
  }
}
