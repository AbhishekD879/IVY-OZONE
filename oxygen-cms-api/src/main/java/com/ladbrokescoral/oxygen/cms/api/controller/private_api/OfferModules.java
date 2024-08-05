package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OfferModule;
import com.ladbrokescoral.oxygen.cms.api.service.OfferModuleService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class OfferModules extends AbstractSortableController<OfferModule> {
  @Autowired
  OfferModules(OfferModuleService crudService) {
    super(crudService);
  }

  @PostMapping("offer-module")
  @Override
  public ResponseEntity create(@RequestBody @Valid OfferModule entity) {
    return super.create(entity);
  }

  @GetMapping("offer-module")
  @Override
  public List<OfferModule> readAll() {
    return super.readAll();
  }

  @GetMapping("offer-module/{id}")
  @Override
  public OfferModule read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("offer-module/brand/{brand}")
  @Override
  public List<OfferModule> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("offer-module/{id}")
  @Override
  public OfferModule update(@PathVariable String id, @RequestBody @Valid OfferModule entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("offer-module/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("offer-module/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
