package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.RemoveCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageEventPublisher;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class RemoveCampaignMessageProcessor extends MessageEventPublisher<RemoveCampaignMessage>
    implements MessageProcessor<RemoveCampaignMessage> {
  private final CampaignRepository campaignRepository;
  private final PostRepository postRepository;

  @Override
  public void process(RemoveCampaignMessage message) {
    campaignRepository.deleteById(message.getAffectedMessageId());

    List<PostMessage> messages = postRepository.findByCampaignId(message.getAffectedMessageId());
    postRepository.deleteAll(messages);
    publish(message);
  }
}
