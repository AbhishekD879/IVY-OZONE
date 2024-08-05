package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.service.SportService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class OlympicSports extends AbstractSortableController<Sport> {
  @Autowired
  OlympicSports(SportService crudService) {
    super(crudService);
  }

  @PostMapping("sports")
  @Override
  public ResponseEntity create(@Validated(Sport.ValidationPost.class) @RequestBody Sport entity) {
    return super.create(entity);
  }

  @GetMapping("sports")
  public ResponseEntity readAll(
      @RequestParam(value = "name", required = false) String sportName,
      @RequestParam(value = "brand") String brand) {
    return new ResponseEntity<>(
        getConcreteService().findAllBySportNameAndBrand(sportName, brand), HttpStatus.OK);
  }

  @GetMapping("sports/{id}")
  @Override
  public Sport read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("sports/{id}")
  @Override
  public Sport update(
      @PathVariable String id, @Validated(Sport.ValidationPut.class) @RequestBody Sport entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("sports/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("sports/{id}/files")
  public ResponseEntity uploadFiles(
      @PathVariable String id,
      @RequestParam(value = "imageFile", required = false) MultipartFile imageFile,
      @RequestParam(value = "icon", required = false) MultipartFile icon,
      @RequestParam(value = "svgIcon", required = false) MultipartFile svg) {
    return getConcreteService()
        .handleUploadedFiles(id, imageFile, icon, svg)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @DeleteMapping("sports/{id}/files")
  public ResponseEntity removeFile(
      @PathVariable String id,
      @RequestParam(value = "fileType", required = true) String[] fileTypes) {
    return getConcreteService()
        .deleteUploadedFiles(id, fileTypes)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @GetMapping("sports/brand/{brand}")
  @Override
  public List<Sport> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  public SportService getConcreteService() {
    return (SportService) crudService;
  }

  @PostMapping("sports/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
