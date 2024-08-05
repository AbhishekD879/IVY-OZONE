package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.PostStatus;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import java.util.Collection;
import java.util.List;
import org.bson.types.ObjectId;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;

public interface TimelinePostPageRepository extends CustomMongoRepository<TimelinePost> {
  Collection<TimelinePost> findByCampaignId(String campaignId);

  List<TimelinePost> findPageByBrandAndCampaignId(
      String brand, String campaignId, Pageable pageable);

  Collection<TimelinePost> findByCampaignIdAndPostStatusIs(String campaignId, PostStatus status);

  List<TimelinePost> findByTemplateId(ObjectId templateId);

  List<TimelinePost> findByBrandAndCampaignId(String brand, String campaignId, Sort sort);

  int countByBrandAndCampaignId(String brand, String campaignId);
}
