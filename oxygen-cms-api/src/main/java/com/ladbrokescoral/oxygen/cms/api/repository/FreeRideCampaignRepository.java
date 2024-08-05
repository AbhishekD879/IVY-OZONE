package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import java.time.Instant;
import java.util.List;

public interface FreeRideCampaignRepository extends CustomMongoRepository<FreeRideCampaign> {

  List<FreeRideCampaign> findAllByBrandAndDisplayFromBetween(
      String brand, Instant today, Instant tomorrow);
}
