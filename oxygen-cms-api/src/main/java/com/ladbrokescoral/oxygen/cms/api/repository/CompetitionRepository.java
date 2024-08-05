package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import java.util.Optional;

public interface CompetitionRepository extends CustomMongoRepository<Competition> {
  Optional<Competition> findByUri(String uri);

  Optional<Competition> findByBrandAndUri(String brand, String uri);

  Optional<Competition> findByBrandAndName(String brand, String name);
}
