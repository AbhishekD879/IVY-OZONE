package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.StructureService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.List;
import java.util.Map;
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
@Validated
public class Structures extends AbstractCrudController<SystemConfiguration> {

  private final StructureService structureService;

  @Autowired
  Structures(StructureService structureService) {
    super(structureService);
    this.structureService = structureService;
  }

  @PostMapping("structure")
  public ResponseEntity<StructureDto> create(@RequestBody @Validated StructureDto entity) {
    return new ResponseEntity<>(
        structureService.updateStructure(entity.getBrand(), entity), HttpStatus.CREATED);
  }

  @GetMapping("structure")
  public List<StructureDto> getAllStructures() {
    return structureService.findAllStructures();
  }

  @GetMapping("structure/brand/{brand}")
  public StructureDto getByBrand(@PathVariable String brand) {
    return structureService.findStructureByBrand(brand).orElseThrow(NotFoundException::new);
  }

  @PutMapping("structure/brand/{brand}")
  public StructureDto update(
      @PathVariable String brand, @RequestBody @Validated StructureDto entity) {
    return structureService.updateStructure(brand, entity);
  }

  @DeleteMapping("structure/brand/{brand}")
  @Override
  public ResponseEntity<SystemConfiguration> delete(@PathVariable String brand) {
    // delete all through configuration api
    structureService.resetToDefaultForBrand(brand);
    return new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }

  @PutMapping("structure/{id}/{elementName}")
  public ResponseEntity<Map<String, Object>> createUpdateElement(
      @PathVariable String id,
      @PathVariable String elementName,
      @RequestBody Map<String, Object> entity) {
    return structureService
        .updateStructureItem(id, elementName, entity)
        .map(structure -> ResponseEntity.ok(entity))
        .orElseGet(notFound());
  }

  @GetMapping("structure/{id}/{elementName}")
  public ResponseEntity<Map<String, Object>> getElement(
      @PathVariable String id, @PathVariable String elementName) {
    return structureService
        .findByBrandAndConfigName(id, elementName)
        .map(element -> new ResponseEntity<>(element, HttpStatus.OK))
        .orElseGet(notFound());
  }

  @DeleteMapping("structure/{id}/{elementName}")
  public ResponseEntity<StructureDto> deleteElement(
      @PathVariable String id, @PathVariable String elementName) {
    return structureService
        .resetToDefaultItem(id, elementName)
        .map(saved -> new ResponseEntity<StructureDto>(HttpStatus.NO_CONTENT))
        .orElseGet(notFound());
  }

  /**
   * Upload image for structure. Example: { "_id" : ObjectId("54d376ac65e1baa68586093b"), "brand" :
   * “bma”, "structure" : { “Element” : { “property1” : "noValue", “myImage” : "noValue" } } } If
   * you want upload image for 'myImage', then url would be:
   * structure/brand/bma/Element/myImage/image
   */
  @PostMapping("structure/brand/{brand}/{elementName}/{propertyName}/image")
  public ResponseEntity<String> uploadImage(
      @PathVariable String brand,
      @PathVariable String elementName,
      @PathVariable String propertyName,
      @ValidFileType({"png", "jpg", "jpeg"}) @RequestParam("file") MultipartFile file) {
    return this.structureService
        .uploadImage(brand, elementName, propertyName, file)
        .map(ResponseEntity::ok)
        .orElseGet(() -> ResponseEntity.badRequest().body("Failed to upload image"));
  }

  @PostMapping("structure/brand/{brand}/{elementName}/{propertyName}/svg")
  public ResponseEntity<String> uploadSvg(
      @PathVariable String brand,
      @PathVariable String elementName,
      @PathVariable String propertyName,
      @RequestParam("file") @ValidFileType({"svg"}) MultipartFile file) {

    return this.structureService
        .uploadSvg(brand, elementName, propertyName, file)
        .map(ResponseEntity::ok)
        .orElseGet(() -> ResponseEntity.badRequest().body("Failed to upload svg"));
  }

  @DeleteMapping("structure/brand/{brand}/{elementName}/{propertyName}/image")
  public ResponseEntity<StructureDto> removeImage(
      @PathVariable String brand,
      @PathVariable String elementName,
      @PathVariable String propertyName) {
    return structureService
        .removeImage(brand, elementName, propertyName)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }
}
