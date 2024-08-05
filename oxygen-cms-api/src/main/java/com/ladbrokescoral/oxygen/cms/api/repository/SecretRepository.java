package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Secret;
import java.util.Optional;

public interface SecretRepository extends CustomMongoRepository<Secret> {
  Optional<Secret> findByBrandAndUriAndEnabledIsTrue(String brand, String uri);
}
