package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.EdpMarket;
import com.ladbrokescoral.oxygen.cms.api.service.EdpMarketService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class EdpMarkets extends AbstractSortableController<EdpMarket> {
  @Autowired
  EdpMarkets(EdpMarketService crudService) {
    super(crudService);
  }

  @PostMapping("edp-market")
  @Override
  public ResponseEntity create(@Validated @RequestBody EdpMarket entity) {
    return super.create(entity);
  }

  @GetMapping("edp-market")
  @Override
  public List<EdpMarket> readAll() {
    return super.readAll();
  }

  @GetMapping("edp-market/{id}")
  @Override
  public EdpMarket read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("edp-market/brand/{brand}")
  @Override
  public List<EdpMarket> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("edp-market/{id}")
  @Override
  public EdpMarket update(@PathVariable String id, @Validated @RequestBody EdpMarket entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("edp-market/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("edp-market/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
