package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesOptinEmailRepository extends CustomMongoRepository<FanzoneOptinEmail> {
  @Query("{'brand': ?0}")
  Optional<FanzoneOptinEmail> findFanzoneOptinEmailByBrand(String brand);
}
