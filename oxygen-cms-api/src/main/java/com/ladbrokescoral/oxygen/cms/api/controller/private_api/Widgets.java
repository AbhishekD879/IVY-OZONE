package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Widget;
import com.ladbrokescoral.oxygen.cms.api.service.WidgetService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Widgets extends AbstractSortableController<Widget> {
  @Autowired
  Widgets(WidgetService crudService) {
    super(crudService);
  }

  @GetMapping("widget")
  @Override
  public List<Widget> readAll() {
    return super.readAll();
  }

  @GetMapping("widget/{id}")
  @Override
  public Widget read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("widget/brand/{brand}")
  @Override
  public List<Widget> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("widget")
  @Override
  public ResponseEntity create(@RequestBody @Valid Widget entity) {
    return super.create(entity);
  }

  @PutMapping("widget/{id}")
  @Override
  public Widget update(@PathVariable String id, @RequestBody @Valid Widget entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("widget/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("widget/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
