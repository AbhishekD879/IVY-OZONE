package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.entity.TimelineChangelogOperation;
import com.ladbrokescoral.oxygen.cms.api.entity.TimelinePostSseEvent;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import java.io.IOException;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@RunWith(MockitoJUnitRunner.class)
public class TimelineSseServiceTest {
  public static final String CAMPAIGN_ID = "123";
  private TimelineSseService service;
  private TimelinePostSseEvent timelinePostSseEvent;

  @Mock private SseEmitter sseEmitter;

  @Before
  public void setUp() {
    TimelinePost post = new TimelinePost();
    post.setCampaignId(CAMPAIGN_ID);

    timelinePostSseEvent = new TimelinePostSseEvent();
    timelinePostSseEvent.setOperation(TimelineChangelogOperation.INSERT);
    timelinePostSseEvent.setCampaignId(CAMPAIGN_ID);
    timelinePostSseEvent.setContent(post);

    service = new TimelineSseService();
    if (TimelineSseService.emitters.size() > 0) {
      TimelineSseService.emitters.remove(0);
    }
    TimelineSseService.emitters.add(sseEmitter);
  }

  @Test
  public void testSendingSseUpdates() throws IOException {
    service.populateEventForReceivers(timelinePostSseEvent);

    verify(sseEmitter).send(any());
    verify(sseEmitter, times(0)).complete();
    assertEquals(1, TimelineSseService.emitters.size());
  }

  @Test
  public void testSseEmitterCompleteCalledOnException() throws IOException {
    doThrow(new IOException()).when(sseEmitter).send(any());
    service.populateEventForReceivers(timelinePostSseEvent);

    verify(sseEmitter).send(any());
    verify(sseEmitter).complete();
    assertEquals(0, TimelineSseService.emitters.size());
  }
}
