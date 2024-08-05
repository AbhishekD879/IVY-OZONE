package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgMigration;
import java.util.Optional;
import org.springframework.data.domain.Sort;

public interface SvgMigrationRepository extends CustomMongoRepository<SvgMigration> {
  Optional<SvgMigration> findFirstByBrand(String brand, Sort sort);
}
