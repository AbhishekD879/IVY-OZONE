package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Badge;
import com.ladbrokescoral.oxygen.cms.api.service.BadgeService;
import javax.validation.Valid;
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
public class BadgeController extends AbstractCrudController<Badge> {

  private BadgeService badgeService;

  BadgeController(BadgeService badgeService) {
    super(badgeService);
    this.badgeService = badgeService;
  }

  @PostMapping("/badge")
  @Override
  public ResponseEntity<Badge> create(@RequestBody @Valid Badge entity) {
    return super.create(entity);
  }

  @PutMapping("/badge/{id}")
  @Override
  public Badge update(@PathVariable String id, @RequestBody @Valid Badge entity) {
    return super.update(id, entity);
  }

  @GetMapping("/badge/brand/{brand}")
  public Badge findByBrand(@PathVariable String brand) {
    return badgeService.findByBrand(brand).stream().findFirst().orElseGet(Badge::new);
  }

  @DeleteMapping("/badge/{id}")
  @Override
  public ResponseEntity<Badge> delete(@PathVariable String id) {
    return super.delete(id);
  }
}
