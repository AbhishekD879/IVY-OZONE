package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybLeague;
import com.ladbrokescoral.oxygen.cms.api.service.BybLeagueService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class BybLeagues extends AbstractSortableController<BybLeague> {

  @Autowired
  BybLeagues(BybLeagueService crudService) {
    super(crudService);
  }

  @GetMapping("byb-league")
  @Override
  public List<BybLeague> readAll() {
    return super.readAll();
  }

  @GetMapping("byb-league/{id}")
  @Override
  public BybLeague read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("byb-league/brand/{brand}")
  @Override
  public List<BybLeague> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("byb-league")
  @Override
  public ResponseEntity create(@RequestBody @Validated BybLeague entity) {
    return super.create(entity);
  }

  @PutMapping("byb-league/{id}")
  @Override
  public BybLeague update(@PathVariable String id, @RequestBody @Validated BybLeague entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("byb-league/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("byb-league/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
