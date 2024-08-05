package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.OtfIosAppToggle;
import java.util.Optional;

public interface OtfIosAppToggleRepository extends CustomMongoRepository<OtfIosAppToggle> {
  Optional<OtfIosAppToggle> findOneByBrand(String brand);

  boolean existsByBrand(String brand);
}
