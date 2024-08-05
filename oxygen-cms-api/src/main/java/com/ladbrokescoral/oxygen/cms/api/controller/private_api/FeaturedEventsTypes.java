package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FeaturedEventsType;
import com.ladbrokescoral.oxygen.cms.api.service.FeaturedEventsTypeService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class FeaturedEventsTypes extends AbstractCrudController<FeaturedEventsType> {
  @Autowired
  FeaturedEventsTypes(FeaturedEventsTypeService crudService) {
    super(crudService);
  }

  @PostMapping("featured-events-type")
  @Override
  public ResponseEntity create(@RequestBody FeaturedEventsType entity) {
    return super.create(entity);
  }

  @GetMapping("featured-events-type")
  @Override
  public List<FeaturedEventsType> readAll() {
    return super.readAll();
  }

  @GetMapping("featured-events-type/{id}")
  @Override
  public FeaturedEventsType read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("featured-events-type/brand/{brand}")
  @Override
  public List<FeaturedEventsType> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("featured-events-type/{id}")
  @Override
  public FeaturedEventsType update(
      @PathVariable String id, @RequestBody FeaturedEventsType entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("featured-events-type/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
