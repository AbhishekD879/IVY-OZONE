package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.League;
import com.ladbrokescoral.oxygen.cms.api.service.LeagueService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class Leagues extends AbstractSortableController<League> {
  @Autowired
  Leagues(LeagueService crudService) {
    super(crudService);
  }

  @PostMapping("league")
  @Override
  public ResponseEntity create(@RequestBody @Valid League entity) {
    return super.create(entity);
  }

  @GetMapping("league")
  @Override
  public List<League> readAll() {
    return super.readAll();
  }

  @GetMapping("league/{id}")
  @Override
  public League read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("league/brand/{brand}")
  @Override
  public List<League> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("league/{id}")
  @Override
  public League update(@PathVariable String id, @RequestBody @Valid League entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("league/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("league/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
