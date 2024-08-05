package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import java.util.Optional;

public interface BrandRepository extends CustomMongoRepository<Brand> {
  Optional<Brand> findOneByBrandCode(final String brandCode);
}
