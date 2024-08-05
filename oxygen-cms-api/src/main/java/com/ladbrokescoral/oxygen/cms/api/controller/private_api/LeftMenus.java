package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LeftMenu;
import com.ladbrokescoral.oxygen.cms.api.service.LeftMenuService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class LeftMenus extends AbstractSortableController<LeftMenu> {
  @Autowired
  LeftMenus(LeftMenuService crudService) {
    super(crudService);
  }

  @PostMapping("left-menu")
  @Override
  public ResponseEntity create(@RequestBody LeftMenu entity) {
    return super.create(entity);
  }

  @GetMapping("left-menu")
  @Override
  public List<LeftMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("left-menu/{id}")
  @Override
  public LeftMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("left-menu/brand/{brand}")
  @Override
  public List<LeftMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("left-menu/{id}")
  @Override
  public LeftMenu update(@PathVariable String id, @RequestBody LeftMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("left-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("left-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
