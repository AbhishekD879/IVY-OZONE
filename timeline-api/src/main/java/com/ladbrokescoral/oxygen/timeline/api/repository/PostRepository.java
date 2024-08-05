package com.ladbrokescoral.oxygen.timeline.api.repository;

import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import java.util.Comparator;
import java.util.List;
import org.springframework.stereotype.Repository;

@Repository
public interface PostRepository extends CustomCrudRepository<PostMessage> {
  Comparator<PostMessage> POST_COMPARATOR =
      Comparator.comparing(PostMessage::getCreatedDate, Comparator.reverseOrder());

  void deleteByCampaignId(String campaignId);

  public List<PostMessage> findByCampaignId(String campaignId);

  public void deleteByIds(List<String> ids);
}
