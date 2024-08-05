package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.service.updates.pubsub.UpdateMessageHandler;
import java.util.List;
import org.springframework.beans.factory.SmartInitializingSingleton;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.dsl.MessageChannels;
import org.springframework.messaging.Message;
import org.springframework.messaging.SubscribableChannel;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
public class SubscriptionConfig {

  @Bean
  public SubscribableChannel messageChannel(
      @Qualifier("threadPoolTaskExecutor") ThreadPoolTaskExecutor threadPoolTaskExecutor) {
    return MessageChannels.publishSubscribe("springIntegrationPubSub", threadPoolTaskExecutor)
        .get();
  }

  @Bean
  UpdateMessageHandler<Message<?>> dispatcherUpdateHandler(
      List<UpdateMessageHandler<Selection>> selectionUpdateHandlers) {
    return message -> {
      if (message.getPayload() instanceof Selection) {
        selectionUpdateHandlers.forEach(
            h -> h.handleUpdateMessage((Selection) message.getPayload()));
      }
    };
  }

  @Bean
  SmartInitializingSingleton subscribeToMessageChannel(
      @Qualifier("messageChannel") SubscribableChannel subscribableChannel,
      List<UpdateMessageHandler<Message<?>>> updateMessageHandlerList) {
    return () ->
        updateMessageHandlerList.forEach(
            handler -> subscribableChannel.subscribe(handler::handleUpdateMessage));
  }
}
