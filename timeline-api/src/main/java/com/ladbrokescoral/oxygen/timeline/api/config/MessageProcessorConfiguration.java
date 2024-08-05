package com.ladbrokescoral.oxygen.timeline.api.config;

import com.ladbrokescoral.oxygen.timeline.api.controller.MessageProcessorFactory;
import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangeCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.RemoveCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.RemovePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.TimelineConfigMessage;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.CampaignMessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.ChangeCampaignMessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.ChangePostMessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.PostMessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.RemoveCampaignMessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.RemovePostMessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.TimelineConfigMessageProcessor;
import java.util.HashMap;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@RequiredArgsConstructor
public class MessageProcessorConfiguration {
  private final PostMessageProcessor postMessageProcessor;
  private final ChangePostMessageProcessor changePostMessagesProcessor;
  private final RemovePostMessageProcessor removePostMessageProcessor;

  private final CampaignMessageProcessor campaignMessageProcessor;
  private final ChangeCampaignMessageProcessor changeCampaignMessageProcessor;
  private final RemoveCampaignMessageProcessor removeCampaignMessageProcessor;
  private final TimelineConfigMessageProcessor timelineConfigMessageProcessor;

  @Bean
  public MessageProcessorFactory messageProcessors() {
    Map<Class<? extends Message>, MessageProcessor<? extends Message>> messageProcessorByType =
        new HashMap<>();

    Class<? extends Message> postMessageClass = PostMessage.class;
    messageProcessorByType.put(postMessageClass, postMessageProcessor);
    messageProcessorByType.put(ChangePostMessage.class, changePostMessagesProcessor);
    messageProcessorByType.put(RemovePostMessage.class, removePostMessageProcessor);

    messageProcessorByType.put(CampaignMessage.class, campaignMessageProcessor);
    messageProcessorByType.put(ChangeCampaignMessage.class, changeCampaignMessageProcessor);
    messageProcessorByType.put(RemoveCampaignMessage.class, removeCampaignMessageProcessor);
    messageProcessorByType.put(TimelineConfigMessage.class, timelineConfigMessageProcessor);
    return new MessageProcessorFactory() {

      @Override
      @SuppressWarnings("unchecked")
      public <T extends Message> MessageProcessor<T> getInstance(Class<?> type) {
        return (MessageProcessor<T>) messageProcessorByType.get(type);
      }
    };
  }
}
