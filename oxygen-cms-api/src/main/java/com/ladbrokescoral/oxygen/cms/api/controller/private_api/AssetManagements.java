package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.service.AssetManagementService;
import java.util.List;
import javax.validation.Valid;
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
public class AssetManagements extends AbstractCrudController<AssetManagement> {

  private final AssetManagementService assetManagementService;

  AssetManagements(AssetManagementService service) {
    super(service);
    this.assetManagementService = service;
  }

  @Override
  @GetMapping("/asset-management")
  public List<AssetManagement> readAll() {
    return super.readAll();
  }

  @Override
  @GetMapping("asset-management/brand/{brand}")
  public List<AssetManagement> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @PostMapping("/asset-management")
  public ResponseEntity create(@Valid @RequestBody AssetManagement entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("/asset-management/{id}")
  public AssetManagement read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/asset-management/{id}")
  public AssetManagement update(
      @PathVariable("id") String id, @Valid @RequestBody AssetManagement updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("/asset-management/{id}")
  public ResponseEntity delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  /**
   * This Method is used for to upload Image in AssetManager
   *
   * @param id
   * @param svgImage
   * @return
   */
  @PostMapping("/asset-management/uploadimage/{id}")
  public AssetManagement uploadImageAssetManager(
      @PathVariable String id,
      @RequestParam(value = "svgImage", required = false) MultipartFile svgImage) {
    return assetManagementService.uploadImageAssetManager(id, svgImage);
  }

  /**
   * This Method is used for to Delete Image in AssetManager
   *
   * @param id
   * @return AssetManagement
   */
  @DeleteMapping("/asset-management/deleteimage/{id}")
  public AssetManagement deleteImageAssetManager(@PathVariable String id) {
    return assetManagementService.deleteImageAssetManager(id);
  }
}
