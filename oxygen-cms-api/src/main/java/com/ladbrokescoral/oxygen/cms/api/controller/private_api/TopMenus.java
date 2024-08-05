package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TopMenu;
import com.ladbrokescoral.oxygen.cms.api.service.TopMenuService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class TopMenus extends AbstractSortableController<TopMenu> {
  @Autowired
  TopMenus(TopMenuService crudService) {
    super(crudService);
  }

  @GetMapping("top-menu")
  @Override
  public List<TopMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("top-menu/{id}")
  @Override
  public TopMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("top-menu/brand/{brand}")
  @Override
  public List<TopMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("top-menu")
  @Override
  public ResponseEntity create(@RequestBody TopMenu entity) {
    return super.create(entity);
  }

  @PutMapping("top-menu/{id}")
  @Override
  public TopMenu update(@PathVariable String id, @RequestBody TopMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("top-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("top-menu/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
