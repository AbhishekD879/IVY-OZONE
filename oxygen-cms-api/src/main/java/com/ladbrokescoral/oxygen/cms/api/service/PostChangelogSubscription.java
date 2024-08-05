package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TimelinePostSseEvent;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class PostChangelogSubscription implements TimelineChangelogSubscription<TimelinePost> {
  private final TimelineSseService timelineSseService;

  @Override
  public void subscribe(TimelineChangelog<TimelinePost> changelog) {
    TimelinePostSseEvent event = new TimelinePostSseEvent();
    event.setOperation(changelog.getOperation());
    event.setContent(changelog.getContent());
    event.setContentId(changelog.getContentId());
    if (event.getContent() != null) {
      event.setCampaignId(changelog.getContent().getCampaignId());
    }

    timelineSseService.populateEventForReceivers(event);
  }

  @Override
  public Class<TimelinePost> type() {
    return TimelinePost.class;
  }
}
