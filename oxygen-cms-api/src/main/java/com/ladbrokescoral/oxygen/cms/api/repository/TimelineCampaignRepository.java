package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.CampaignStatus;
import java.time.Instant;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface TimelineCampaignRepository extends CustomMongoRepository<Campaign> {
  @Query(
      value =
          "{'brand' : ?0, 'displayFrom':{ $lte: ?1}, 'displayTo':{ $gte: ?1}, 'status': 'LIVE'}")
  Optional<Campaign> findCurrentLiveCampaignByBrand(String brand, Instant now1);

  Optional<Campaign> findByIdIsNotAndBrandAndStatusAndDisplayToIsAfter(
      String id, String brand, CampaignStatus status, Instant displayTo);
}
