package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import java.util.Optional;

public interface RssRepository extends CustomMongoRepository<RssReward> {
  Optional<RssReward> findOneByBrand(String brand);

  void deleteByBrand(String brand);
}
