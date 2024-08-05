package com.ladbrokescoral.oxygen.timeline.api.repository;

import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import org.springframework.stereotype.Repository;

@Repository
public interface CampaignRepository extends CustomCrudRepository<CampaignMessage> {}
