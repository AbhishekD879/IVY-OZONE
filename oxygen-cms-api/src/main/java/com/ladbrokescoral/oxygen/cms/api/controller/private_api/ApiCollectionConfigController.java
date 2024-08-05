package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ApiCollectionConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.service.ApiCollectionConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class ApiCollectionConfigController extends AbstractCrudController<ApiCollectionConfig> {
  private ApiCollectionConfigService apiCollectionConfigService;
  private CrudService<User> userService;

  @Autowired
  ApiCollectionConfigController(
      ApiCollectionConfigService apiCollectionConfigService, CrudService<User> userService) {
    super(apiCollectionConfigService);
    this.apiCollectionConfigService = apiCollectionConfigService;
    this.userService = userService;
  }

  @PostMapping("/api-collection-config")
  public ResponseEntity<ApiCollectionConfig> createConfigMap(
      @Valid @RequestBody ApiCollectionConfigDto apiCollectionConfigDto) {
    ApiCollectionConfig apiCollConfig = new ApiCollectionConfig();
    BeanUtils.copyProperties(apiCollectionConfigDto, apiCollConfig);
    apiCollectionConfigService.validateConfigMapByKey(apiCollConfig);
    return super.create(
        apiCollectionConfigService.populateCreatorAndUpdater(
            userService, apiCollConfig.prepareModelBeforeSave()));
  }

  @PutMapping("/api-collection-config/{brand}/{column}/{id}")
  public ApiCollectionConfig update(
      @Valid @RequestBody ApiCollectionConfigDto apiCollectionConfigDto,
      @PathVariable String brand,
      @PathVariable String column,
      @PathVariable String id) {
    ApiCollectionConfig apiCollConfigEntity = new ApiCollectionConfig();
    BeanUtils.copyProperties(apiCollectionConfigDto, apiCollConfigEntity);
    ApiCollectionConfig apiCollectionConfig =
        apiCollectionConfigService.findConfigMapByBrandAndColumn(brand, column, id);
    return super.update(
        apiCollectionConfig.getId(),
        apiCollectionConfigService.populateCreatorAndUpdater(
            userService, apiCollConfigEntity.prepareModelBeforeUpdate()));
  }

  /**
   * Method description It will get all entries from ConfigMap based on brand name. @Param brand
   * represent the brand name @Return List<ApiCollectionConfig>
   */
  @GetMapping("/api-collection-config/{brand}")
  public Optional<List<ApiCollectionConfig>> getAllConfigMapByBrand(@PathVariable String brand) {
    return apiCollectionConfigService.findAllConfigMapByBrand(brand);
  }

  /**
   * Method description It will get one specific entry from ConfigMap based on column & its
   * value @Param brand,column, value @Return ApiCollectionConfig
   */
  @GetMapping("/api-collection-config/{brand}/{column}/{value}")
  public ApiCollectionConfig getConfigMapById(
      @PathVariable String brand, @PathVariable String column, @PathVariable String value) {
    return apiCollectionConfigService.findConfigMapByBrandAndColumn(brand, column, value);
  }
  /**
   * Method description It will delete one specific entry from ConfigMap based on brand, column &
   * its value @Param brand,column, value
   */
  @DeleteMapping("/api-collection-config/{brand}/{column}/{value}")
  public void deleteConfigEntryByID(
      @PathVariable String brand, @PathVariable String column, @PathVariable String value) {
    apiCollectionConfigService.deleteByBrandAndColumn(brand, column, value);
  }

  /**
   * Method description It will delete all ConfigMap entries by brand @Param brand represent the
   * brand name
   */
  @DeleteMapping("/api-collection-config/{brand}")
  public void deleteAllConfigMapByBrand(@PathVariable String brand) {
    apiCollectionConfigService.deleteAllByBrand(brand);
  }
}
