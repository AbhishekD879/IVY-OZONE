package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageEventPublisher;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class CampaignMessageProcessor extends MessageEventPublisher<CampaignMessage>
    implements MessageProcessor<CampaignMessage> {
  private final CampaignRepository campaignRepository;

  @Override
  public void process(CampaignMessage postMessage) {
    postMessage = campaignRepository.save(postMessage);
    publish(postMessage);
  }
}
