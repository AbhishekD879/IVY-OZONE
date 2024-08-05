package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import java.util.List;
import java.util.Optional;

public interface SystemConfigurationRepository extends CustomMongoRepository<SystemConfiguration> {

  Optional<SystemConfiguration> findOneByBrand(String brand);

  void deleteAllByBrand(String brand);

  Optional<SystemConfiguration> findOneByBrandAndName(String brand, String name);

  List<SystemConfiguration> findAllByBrandAndIsInitialDataConfigIsTrue(String brand);
}
