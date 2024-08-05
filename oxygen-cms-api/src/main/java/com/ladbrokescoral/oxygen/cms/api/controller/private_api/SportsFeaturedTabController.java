package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.SimpleModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportsFeaturedTab;
import com.ladbrokescoral.oxygen.cms.api.service.SportsFeaturedTabService;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class SportsFeaturedTabController extends AbstractCrudController<SportsFeaturedTab> {
  SportsFeaturedTabController(SportsFeaturedTabService crudService) {
    super(crudService);
  }

  @GetMapping("sports-featured-tab")
  @Override
  public List<SportsFeaturedTab> readAll() {
    return super.readAll();
  }

  @GetMapping("/sports-featured-tab/{id}")
  @Override
  public SportsFeaturedTab read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("/sports-featured-tab/brand/{brand}")
  @Override
  public List<SportsFeaturedTab> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("sports-featured-tab")
  @Override
  public ResponseEntity create(@Valid @RequestBody SportsFeaturedTab entity) {
    // not saving modules while inserting whole structure to avoid complications with bulk modules
    // insert
    entity.setModules(Collections.emptyList());
    return super.create(entity);
  }

  @PutMapping("/sports-featured-tab/{id}")
  @Override
  public SportsFeaturedTab update(
      @PathVariable String id, @Valid @RequestBody SportsFeaturedTab updateEntity) {
    // not changing modules while updating whole structure to avoid complications with bulk modules
    // update
    Optional<SportsFeaturedTab> maybeEntity = crudService.findOne(id);
    maybeEntity.ifPresent(e -> updateEntity.setModules(e.getModules()));
    return super.update(maybeEntity, updateEntity);
  }

  @DeleteMapping("/sports-featured-tab/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("/sports-featured-tab/{id}/module")
  public ResponseEntity createModule(
      @PathVariable String id, @Valid @RequestBody SimpleModule module) {
    return getConcreteService()
        .addNewModule(id, module)
        .flatMap(ft -> ft.getModule(module.getId()))
        .map(newModule -> new ResponseEntity<>(newModule, HttpStatus.CREATED))
        .orElseGet(notFound());
  }

  @GetMapping("/sports-featured-tab/{id}/module")
  public ResponseEntity getModule(@PathVariable String id) {
    return getConcreteService().getModules(id).map(ResponseEntity::ok).orElseGet(notFound());
  }

  @GetMapping("/sports-featured-tab/{id}/module/{moduleId}")
  public ResponseEntity getModule(@PathVariable String id, @PathVariable String moduleId) {
    return getConcreteService()
        .getModule(id, moduleId)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @PutMapping("/sports-featured-tab/{id}/module/{moduleId}")
  public ResponseEntity updateModule(
      @PathVariable String id,
      @PathVariable String moduleId,
      @Valid @RequestBody SimpleModule module) {
    module.setId(moduleId);
    return getConcreteService()
        .updateModule(id, module)
        .flatMap(ft -> ft.getModule(moduleId))
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @DeleteMapping("/sports-featured-tab/{id}/module/{moduleId}")
  public ResponseEntity deleteModule(@PathVariable String id, @PathVariable String moduleId) {
    return getConcreteService().removeModule(id, moduleId).map(noContent()).orElseGet(notFound());
  }

  private SportsFeaturedTabService getConcreteService() {
    return (SportsFeaturedTabService) crudService;
  }
}
