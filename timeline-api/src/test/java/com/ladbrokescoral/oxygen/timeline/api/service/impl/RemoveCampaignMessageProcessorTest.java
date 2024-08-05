package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.timeline.api.model.message.RemoveCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.time.Instant;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.ApplicationEventPublisher;

@RunWith(MockitoJUnitRunner.class)
public class RemoveCampaignMessageProcessorTest {
  @Mock private ApplicationEventPublisher eventPublisher;
  @InjectMocks private RemoveCampaignMessageProcessor removeCampaignMessageProcessor;
  @Mock CampaignRepository campaignRepository;
  @Mock PostRepository postRepository;

  @Test(expected = NullPointerException.class)
  public void deleteMethod() {
    RemoveCampaignMessage removeCampaignMessage = new RemoveCampaignMessage();
    removeCampaignMessage.setBrand("coral");
    removeCampaignMessage.setAffectedMessageId("12345");
    Instant instant = Instant.now();
    removeCampaignMessage.setCreatedDate(instant);
    removeCampaignMessage.setId("12345");
    removeCampaignMessage.setAffectedMessageCreatedDate(instant);
    removeCampaignMessageProcessor.process(removeCampaignMessage);
  }
}
