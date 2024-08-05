package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.abstractions.WysiwygControllerTraits;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FeatureService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import java.util.List;
import javax.validation.constraints.NotBlank;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
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
public class Features extends AbstractImageController<Feature>
    implements WysiwygControllerTraits<Feature> {

  private final FeatureService featureService;
  private final WysiwygService wysiwygService;

  @Autowired
  Features(FeatureService crudService, WysiwygService wysiwygService) {
    super(crudService);
    this.featureService = crudService;
    this.wysiwygService = wysiwygService;
  }

  @PostMapping("feature")
  @Override
  public ResponseEntity create(@RequestBody Feature entity) {
    return super.create(entity);
  }

  @GetMapping("feature")
  @Override
  public List<Feature> readAll() {
    return super.readAll();
  }

  @GetMapping("feature/{id}")
  @Override
  public Feature read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("feature/brand/{brand}")
  @Override
  public List<Feature> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("feature/{id}")
  @Override
  public Feature update(@PathVariable String id, @RequestBody Feature entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("feature/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("feature/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("feature/{id}/wysiwyg-image")
  public ResponseEntity uploadWysiwygImage(
      @RequestParam("file") MultipartFile file, @PathVariable("id") @NotBlank String id) {
    return featureService
        .findOne(id)
        .map(Feature::getBrand)
        .map(brand -> uploadWysiwygImage(brand, file, Feature.COLLECTION_NAME, id))
        .orElseGet(notFound());
  }

  @DeleteMapping("feature/{id}/wysiwyg-image/{imageName}")
  public ResponseEntity removeWysiwygImage(
      @PathVariable("id") @NotBlank String id, @PathVariable("imageName") String imageName) {
    return featureService
        .findOne(id)
        .map(Feature::getBrand)
        .map(brand -> removeWysiwygImage(brand, id, Feature.COLLECTION_NAME, imageName))
        .orElseGet(notFound());
  }

  @Override
  public CrudService<Feature> getCRUDService() {
    return this.featureService;
  }

  @Override
  public WysiwygService getWysiwygService() {
    return this.wysiwygService;
  }

  @PostMapping("feature/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    return featureService
        .findOne(id)
        .flatMap(betReceipt -> featureService.attachImage(betReceipt, file))
        .map(featureService::save)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @DeleteMapping("feature/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Feature feature = featureService.findOne(id).orElseThrow(NotFoundException::new);

    return featureService
        .removeImages(feature)
        .map(featureService::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }
}
