package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.NetworkIndicatorConfig;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public interface NetworkIndicatorRepository extends CustomMongoRepository<NetworkIndicatorConfig> {
  Optional<NetworkIndicatorConfig> findOneByBrand(String brand);
}
