package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.ExtraNavigationPointService;
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
@SuppressWarnings("java:S4684")
public class ExtraNavigationPointController
    extends AbstractSortableController<ExtraNavigationPoint> {

  @Autowired
  public ExtraNavigationPointController(ExtraNavigationPointService service) {
    super(service);
  }

  @GetMapping("extra-navigation-points/brand/{brand}")
  @Override
  public List<ExtraNavigationPoint> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("extra-navigation-points/{id}")
  @Override
  public ExtraNavigationPoint read(@PathVariable String id) {
    return super.read(id);
  }

  @PostMapping("extra-navigation-points")
  @Override
  public ResponseEntity<ExtraNavigationPoint> create(
      @RequestBody @Valid ExtraNavigationPoint entity) {
    return super.create(entity);
  }

  @PutMapping("extra-navigation-points/{id}")
  @Override
  public ExtraNavigationPoint update(
      @PathVariable String id, @RequestBody @Valid ExtraNavigationPoint entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("extra-navigation-points/{id}")
  @Override
  public ResponseEntity<ExtraNavigationPoint> delete(@PathVariable String id) {
    return super.delete(id);
  }

  @Override
  @PostMapping("extra-navigation-points/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
