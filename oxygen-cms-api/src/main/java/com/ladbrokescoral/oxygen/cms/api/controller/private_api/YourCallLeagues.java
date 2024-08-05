package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallLeague;
import com.ladbrokescoral.oxygen.cms.api.service.YourCallLeagueService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class YourCallLeagues extends AbstractSortableController<YourCallLeague> {

  @Autowired
  YourCallLeagues(YourCallLeagueService crudService) {
    super(crudService);
  }

  @GetMapping("your-call-league")
  @Override
  public List<YourCallLeague> readAll() {
    return super.readAll();
  }

  @GetMapping("your-call-league/{id}")
  @Override
  public YourCallLeague read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("your-call-league/brand/{brand}")
  @Override
  public List<YourCallLeague> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("your-call-league")
  @Override
  public ResponseEntity create(@RequestBody @Validated YourCallLeague entity) {
    return super.create(entity);
  }

  @PutMapping("your-call-league/{id}")
  @Override
  public YourCallLeague update(
      @PathVariable String id, @RequestBody @Validated YourCallLeague entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("your-call-league/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("your-call-league/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
