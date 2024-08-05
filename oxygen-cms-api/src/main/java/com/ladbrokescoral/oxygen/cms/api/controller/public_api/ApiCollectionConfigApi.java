package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.api.service.ApiCollectionConfigService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ApiCollectionConfigApi implements Public {

  private ApiCollectionConfigService apiCollectionConfigService;

  @Autowired
  public ApiCollectionConfigApi(ApiCollectionConfigService apiCollectionConfigService) {
    this.apiCollectionConfigService = apiCollectionConfigService;
  }

  /**
   * Method description It will get all entries from ConfigMap based on brand name. @Param brand
   * represent the brand name @Return List<ApiCollectionConfig>
   */
  @GetMapping("/api-collection-config/{brand}")
  public Optional<List<ApiCollectionConfig>> findAllConfigMapByBrand(
      @PathVariable("brand") String brand) {
    return apiCollectionConfigService.findAllConfigMapByBrand(brand);
  }
}
