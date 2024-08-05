package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.EventHub;
import java.util.Optional;

public interface EventHubRepository
    extends CustomMongoRepository<EventHub>, FindByRepository<EventHub> {

  Optional<EventHub> findOneByBrandAndIndexNumber(String brand, Integer pageId);
}
