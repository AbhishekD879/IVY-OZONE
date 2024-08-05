package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangeCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import java.time.Instant;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.ApplicationEventPublisher;

@Slf4j
@RunWith(MockitoJUnitRunner.class)
public class ChangeCampaignMessageProcessorTest {
  @Mock ApplicationEventPublisher eventPublisher;
  @InjectMocks ChangeCampaignMessageProcessor changeCampaignMessageProcessor;
  @Mock CampaignRepository campaignRepository;

  @Test(expected = NullPointerException.class)
  public void savetest() {
    ChangeCampaignMessage postMessage = new ChangeCampaignMessage();
    postMessage.setId("12345");
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    CampaignMessage campaignMessage = new CampaignMessage();
    campaignMessage.setBrand("coral");
    campaignMessage.setCreatedDate(instant);
    campaignMessage.setId("12345");
    postMessage.setData(campaignMessage);
    campaignRepository.save(postMessage.getData());
    changeCampaignMessageProcessor.process(postMessage);
  }
}
