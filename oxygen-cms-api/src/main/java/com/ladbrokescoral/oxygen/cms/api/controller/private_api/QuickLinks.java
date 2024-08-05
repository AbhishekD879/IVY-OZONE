package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QuickLink;
import com.ladbrokescoral.oxygen.cms.api.service.QuickLinkService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class QuickLinks extends AbstractSortableController<QuickLink> {
  @Autowired
  QuickLinks(QuickLinkService crudService) {
    super(crudService);
  }

  @GetMapping("quick-link")
  @Override
  public List<QuickLink> readAll() {
    return super.readAll();
  }

  @GetMapping("quick-link/{id}")
  @Override
  public QuickLink read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("quick-link/brand/{brand}")
  @Override
  public List<QuickLink> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("quick-link")
  @Override
  public ResponseEntity create(@RequestBody QuickLink entity) {
    return super.create(entity);
  }

  @PutMapping("quick-link/{id}")
  @Override
  public QuickLink update(@PathVariable String id, @RequestBody QuickLink entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("quick-link/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("quick-link/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
