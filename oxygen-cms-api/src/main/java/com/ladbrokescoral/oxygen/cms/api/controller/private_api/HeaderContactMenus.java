package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderContactMenu;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderContactMenuService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class HeaderContactMenus extends AbstractSortableController<HeaderContactMenu> {
  @Autowired
  public HeaderContactMenus(HeaderContactMenuService crudService) {
    super(crudService);
  }

  @PostMapping("header-contact-menu")
  @Override
  public ResponseEntity create(@RequestBody HeaderContactMenu entity) {
    return super.create(entity);
  }

  @GetMapping("header-contact-menu")
  @Override
  public List<HeaderContactMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("header-contact-menu/{id}")
  @Override
  public HeaderContactMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("header-contact-menu/brand/{brand}")
  @Override
  public List<HeaderContactMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("header-contact-menu/{id}")
  @Override
  public HeaderContactMenu update(@PathVariable String id, @RequestBody HeaderContactMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("header-contact-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("header-contact-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
