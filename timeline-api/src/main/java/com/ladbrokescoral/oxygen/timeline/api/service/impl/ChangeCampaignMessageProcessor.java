package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangeCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageEventPublisher;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class ChangeCampaignMessageProcessor extends MessageEventPublisher<ChangeCampaignMessage>
    implements MessageProcessor<ChangeCampaignMessage> {
  private final CampaignRepository campaignRepository;

  @Override
  public void process(ChangeCampaignMessage message) {
    message.setId(message.getAffectedMessageId());
    campaignRepository.save(message.getData());
    publish(message);
  }
}
