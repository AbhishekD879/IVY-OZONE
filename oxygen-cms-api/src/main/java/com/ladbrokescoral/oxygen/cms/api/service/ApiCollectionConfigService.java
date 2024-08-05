package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.ConfigMapKeyDuplicationException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.ApiCollectionConfigRepository;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.validation.constraints.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ApiCollectionConfigService extends AbstractService<ApiCollectionConfig> {

  private ApiCollectionConfigRepository apiCollectionConfigRepository;

  @Autowired
  public ApiCollectionConfigService(ApiCollectionConfigRepository apiCollectionConfigRepository) {
    super(apiCollectionConfigRepository);
    this.apiCollectionConfigRepository = apiCollectionConfigRepository;
  }

  public Optional<List<ApiCollectionConfig>> findAllConfigMapByBrand(String brand) {
    return apiCollectionConfigRepository.findAllConfigMapByBrand(brand);
  }

  public ApiCollectionConfig findConfigMapByBrandAndColumn(
      String brand, String column, String val) {
    Optional<ApiCollectionConfig> apiCollectionConfig =
        apiCollectionConfigRepository.findConfigMapByAndColumn(brand, column, val);
    return apiCollectionConfig.isPresent() ? apiCollectionConfig.get() : new ApiCollectionConfig();
  }

  public void deleteByBrandAndColumn(String brand, String column, String value) {
    ApiCollectionConfig apiCollectionConfig =
        apiCollectionConfigRepository
            .findConfigMapByAndColumn(brand, column, value)
            .orElseThrow(NotFoundException::new);
    apiCollectionConfigRepository.delete(apiCollectionConfig);
  }

  public void deleteAllByBrand(String brand) {
    Optional<List<ApiCollectionConfig>> apiCollectionConfigs =
        apiCollectionConfigRepository.findAllConfigMapByBrand(brand);
    if (apiCollectionConfigs.isPresent()) {
      apiCollectionConfigs.get().stream()
          .forEach(collectionConfig -> apiCollectionConfigRepository.delete(collectionConfig));
    } else throw new NotFoundException();
  }

  public ApiCollectionConfig populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull ApiCollectionConfig entity) {
    Optional.ofNullable(entity.getCreatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userServiceObj::findOne)
        .ifPresent(user -> entity.setCreatedByUserName(user.getEmail()));

    Optional.ofNullable(entity.getUpdatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userServiceObj::findOne)
        .ifPresent(user -> entity.setUpdatedByUserName(user.getEmail()));
    return entity;
  }

  public void validateConfigMapByKey(ApiCollectionConfig apiCollectionConfig) {
    Optional<List<ApiCollectionConfig>> apiCollectionConfigList =
        findAllConfigMapByBrand(apiCollectionConfig.getBrand());
    if (apiCollectionConfigList.isPresent()) {
      List<String> configMapKey =
          apiCollectionConfigList.get().stream()
              .map(configMap -> configMap.getKey().toUpperCase())
              .collect(Collectors.toList());
      if (configMapKey.contains(apiCollectionConfig.getKey().toUpperCase())) {
        throw new ConfigMapKeyDuplicationException(
            "Duplicate Key will not be allow " + apiCollectionConfig.getKey());
      }
    }
  }
}
