package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.entity.TimelineChangelogOperation;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class PostChangelogSubscriptionTest {
  public static final String CAMPAIGN_ID = "123";

  private PostChangelogSubscription subscription;

  private TimelineChangelog<TimelinePost> changelogInfo;
  @Mock TimelineSseService sseService;

  @Before
  public void setUp() {
    TimelinePost post = new TimelinePost();
    post.setCampaignId(CAMPAIGN_ID);
    changelogInfo = new TimelineChangelog<>();
    changelogInfo.setOperation(TimelineChangelogOperation.INSERT);
    changelogInfo.setContent(post);
    subscription = new PostChangelogSubscription(sseService);
  }

  @Test
  public void testPostChangeLogCallsSseService() {
    subscription.subscribe(changelogInfo);

    verify(sseService).populateEventForReceivers(any());
  }
}
