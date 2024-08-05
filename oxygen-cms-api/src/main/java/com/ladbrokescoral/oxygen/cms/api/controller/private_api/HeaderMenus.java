package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderMenu;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderMenuService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class HeaderMenus extends AbstractSortableController<HeaderMenu> {
  @Autowired
  HeaderMenus(HeaderMenuService crudService) {
    super(crudService);
  }

  @PostMapping("header-menu")
  @Override
  public ResponseEntity create(@RequestBody HeaderMenu entity) {
    return super.create(entity);
  }

  @GetMapping("header-menu")
  @Override
  public List<HeaderMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("header-menu/{id}")
  @Override
  public HeaderMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("header-menu/brand/{brand}")
  @Override
  public List<HeaderMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("header-menu/{id}")
  @Override
  public HeaderMenu update(@PathVariable String id, @RequestBody HeaderMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("header-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("header-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
