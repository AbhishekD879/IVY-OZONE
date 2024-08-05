package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationPointService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.SegmentNamePattern;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Validated
public class NavigationPoints extends AbstractSortableController<NavigationPoint> {

  private final NavigationPointService navigationService;

  public NavigationPoints(NavigationPointService navigationService) {
    super(navigationService);
    this.navigationService = navigationService;
  }

  @GetMapping("navigation-points")
  @Override
  public List<NavigationPoint> readAll() {
    return super.readAll();
  }

  @GetMapping("navigation-points/brand/{brand}")
  @Override
  public List<NavigationPoint> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("navigation-points/{id}")
  @Override
  public NavigationPoint read(@PathVariable String id) {
    return super.read(id);
  }

  @PostMapping("navigation-points")
  @Override
  public ResponseEntity create(@RequestBody @Validated NavigationPoint entity) {
    return super.create(entity);
  }

  @PutMapping("navigation-points/{id}")
  @Override
  public NavigationPoint update(
      @PathVariable String id, @RequestBody @Validated NavigationPoint entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("navigation-points/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("navigation-points/brand/{brand}/segment/{segmentName}")
  public List<NavigationPoint> readByBrandAndSegmentName(
      @PathVariable @Brand String brand, @PathVariable @SegmentNamePattern String segmentName) {
    return navigationService.findByBrandAndSegmentName(brand, segmentName);
  }

  @Override
  @PostMapping("navigation-points/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
