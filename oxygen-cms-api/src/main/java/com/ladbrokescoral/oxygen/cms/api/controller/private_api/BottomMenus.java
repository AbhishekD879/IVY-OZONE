package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BottomMenu;
import com.ladbrokescoral.oxygen.cms.api.service.BottomMenuService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class BottomMenus extends AbstractSortableController<BottomMenu> {
  @Autowired
  public BottomMenus(BottomMenuService crudService) {
    super(crudService);
  }

  @PostMapping("bottom-menu")
  @Override
  public ResponseEntity create(@RequestBody BottomMenu entity) {
    return super.create(entity);
  }

  @GetMapping("bottom-menu")
  @Override
  public List<BottomMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("bottom-menu/{id}")
  @Override
  public BottomMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("bottom-menu/brand/{brand}")
  @Override
  public List<BottomMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("bottom-menu/{id}")
  @Override
  public BottomMenu update(@PathVariable String id, @RequestBody BottomMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("bottom-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("bottom-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
