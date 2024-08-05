package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class Brands extends AbstractSortableController<Brand> {
  @Autowired
  public Brands(BrandService crudService) {
    super(crudService);
  }

  @PostMapping("brand")
  @Override
  public ResponseEntity create(@RequestBody @Validated Brand entity) {
    return super.create(entity);
  }

  @GetMapping("brand")
  @Override
  public List<Brand> readAll() {
    return super.readAll();
  }

  @GetMapping("brand/{id}")
  @Override
  public Brand read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("brand/{id}")
  @Override
  public Brand update(@PathVariable String id, @RequestBody @Validated Brand entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("brand/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @Override
  @PostMapping("brand/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
