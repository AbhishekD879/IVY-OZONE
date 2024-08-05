package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.TimelineConfigMessage;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageEventPublisher;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class TimelineConfigMessageProcessor extends MessageEventPublisher<TimelineConfigMessage>
    implements MessageProcessor<TimelineConfigMessage> {

  @Override
  public void process(TimelineConfigMessage timelineConfigMessage) {
    publish(timelineConfigMessage);
  }
}
