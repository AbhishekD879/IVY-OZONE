package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderSubMenu;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderSubMenuService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class HeaderSubMenus extends AbstractSortableController<HeaderSubMenu> {
  @Autowired
  HeaderSubMenus(HeaderSubMenuService crudService) {
    super(crudService);
  }

  @PostMapping("header-submenu")
  @Override
  public ResponseEntity create(@RequestBody HeaderSubMenu entity) {
    return super.create(entity);
  }

  @GetMapping("header-submenu")
  @Override
  public List<HeaderSubMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("header-submenu/{id}")
  @Override
  public HeaderSubMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("header-submenu/brand/{brand}")
  @Override
  public List<HeaderSubMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("header-submenu/{id}")
  @Override
  public HeaderSubMenu update(@PathVariable String id, @RequestBody HeaderSubMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("header-submenu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("header-submenu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
