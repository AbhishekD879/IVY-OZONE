package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface ApiCollectionConfigRepository extends CustomMongoRepository<ApiCollectionConfig> {
  @Query("{'brand': ?0}")
  Optional<List<ApiCollectionConfig>> findAllConfigMapByBrand(String brand);

  @Query("{'brand': ?0,'?1': ?2}")
  Optional<ApiCollectionConfig> findConfigMapByAndColumn(String brand, String column, String val);
}
