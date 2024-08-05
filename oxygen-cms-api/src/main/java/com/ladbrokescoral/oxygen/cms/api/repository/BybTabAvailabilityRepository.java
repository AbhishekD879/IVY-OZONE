package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BybTabAvailability;
import java.util.Optional;

public interface BybTabAvailabilityRepository extends CustomMongoRepository<BybTabAvailability> {
  Optional<BybTabAvailability> findOneByBrandAndDevice(String brand, String device);
}
