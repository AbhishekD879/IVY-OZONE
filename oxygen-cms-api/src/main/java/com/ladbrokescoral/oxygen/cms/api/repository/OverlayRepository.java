package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import java.util.Optional;

/** Overlay Repository */
public interface OverlayRepository extends CustomMongoRepository<Overlay> {
  Optional<Overlay> findOneByBrand(String brand);
}
