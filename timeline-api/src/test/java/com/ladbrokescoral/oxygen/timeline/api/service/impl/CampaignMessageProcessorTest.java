package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import java.time.Instant;
import lombok.extern.slf4j.Slf4j;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.ApplicationEventPublisher;

@Slf4j
@RunWith(MockitoJUnitRunner.class)
public class CampaignMessageProcessorTest {
  @Mock private ApplicationEventPublisher eventPublisher;
  @InjectMocks CampaignMessageProcessor campaignMessageProcessor;
  @Mock CampaignRepository campaignRepository;

  @Before
  public void init() {
    CampaignMessage postMessage = new CampaignMessage();
    postMessage.setId("12345");
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    postMessage.setPageSize(10);
    doReturn(postMessage).when(campaignRepository).save(any(CampaignMessage.class));
  }

  @Test(expected = NullPointerException.class)
  public void savetest() {
    CampaignMessage postMessage = new CampaignMessage();
    postMessage.setId("12345");
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    postMessage.setPageSize(10);
    CampaignMessage saved = campaignRepository.save(postMessage);
    campaignMessageProcessor.process(postMessage);
  }
}
