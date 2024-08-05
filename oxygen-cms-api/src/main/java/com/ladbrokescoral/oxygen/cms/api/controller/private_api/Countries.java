package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import com.ladbrokescoral.oxygen.cms.api.service.CountryService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class Countries extends AbstractCrudController<Country> {

  private final CountryService countryService;

  @Autowired
  Countries(CountryService countryService) {
    super(countryService);
    this.countryService = countryService;
  }

  @PostMapping("country")
  @Override
  public ResponseEntity create(@RequestBody @Validated Country entity) {
    return super.create(entity);
  }

  @GetMapping("country")
  @Override
  public List<Country> readAll() {
    return super.readAll();
  }

  @GetMapping("country/{id}")
  @Override
  public Country read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("country/brand/{brand}")
  @Override
  public List<Country> readByBrand(@PathVariable String brand) {
    List<Country> countries = countryService.findByBrand(brand);
    countries = super.populateCreatorAndUpdater(countries);
    return countries;
  }

  @PutMapping("country/{id}")
  @Override
  public Country update(@PathVariable String id, @RequestBody @Validated Country entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("country/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
