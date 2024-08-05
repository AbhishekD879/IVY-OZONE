package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import com.ladbrokescoral.oxygen.cms.api.service.BybMarketService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class BybMarkets extends AbstractSortableController<BybMarket> {
  @Autowired
  BybMarkets(BybMarketService crudService) {
    super(crudService);
  }

  @Override
  @GetMapping("byb-market")
  public List<BybMarket> readAll() {
    return super.readAll();
  }

  @Override
  @PostMapping("byb-market")
  public ResponseEntity create(@Validated @RequestBody BybMarket entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("byb-market/brand/{brand}")
  public List<BybMarket> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @GetMapping("byb-market/{id}")
  public BybMarket read(@PathVariable String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("byb-market/{id}")
  public BybMarket update(@PathVariable String id, @Validated @RequestBody BybMarket updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("byb-market/{id}")
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("byb-market/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
