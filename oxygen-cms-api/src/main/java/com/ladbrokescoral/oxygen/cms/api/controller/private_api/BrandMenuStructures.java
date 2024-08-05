package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BrandMenuStructure;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.BrandMenuStructureService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class BrandMenuStructures extends AbstractSortableController<BrandMenuStructure> {
  @Autowired
  public BrandMenuStructures(BrandMenuStructureService crudService) {
    super(crudService);
  }

  @GetMapping("menu-structure")
  @Override
  public List<BrandMenuStructure> readAll() {
    return super.readAll();
  }

  @GetMapping("menu-structure/{id}")
  @Override
  public BrandMenuStructure read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("menu-structure/brand/{brand}")
  public BrandMenuStructure findByBrand(@PathVariable String brand) {
    return crudService.findByBrand(brand).stream().findFirst().orElseThrow(NotFoundException::new);
  }

  @DeleteMapping("menu-structure/{id}")
  public ResponseEntity deleteByBrand(@PathVariable String id) {
    return super.delete(id);
  }

  @PutMapping("menu-structure/{id}")
  @Override
  public BrandMenuStructure update(
      @PathVariable String id, @RequestBody @Validated BrandMenuStructure menuStructure) {
    return super.update(crudService.findOne(id), menuStructure);
  }

  @PostMapping("menu-structure")
  public ResponseEntity create(@RequestBody @Validated BrandMenuStructure menuStructure) {
    Optional<BrandMenuStructure> maybeStructure =
        crudService.findByBrand(menuStructure.getBrand()).stream().findFirst();
    return maybeStructure
        .map(entity -> new ResponseEntity(HttpStatus.CONFLICT))
        .orElse(super.create(menuStructure));
  }
}
