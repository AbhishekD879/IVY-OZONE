package com.egalacoral.spark.liveserver.configuration;

import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisherTopicSelector;
import com.egalacoral.spark.liveserver.service.LiveServerMessageHandler;
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage;
import com.egalacoral.spark.liveserver.utils.JsonMapper;

/** Created by Aliaksei Yarotski on 11/7/17. */
public class LiveServerHandlerConfiguration {

  private MessagePublisher messagePublisher;
  private MessagePublisherTopicSelector topicSelector;
  private LiveServerSubscriptionsQAStorage lsQAStorage;
  private JsonMapper jsonMapper;
  private long expireAfterWrite;

  public LiveServerHandlerConfiguration messagePublisher(MessagePublisher messagePublisher) {
    this.messagePublisher = messagePublisher;
    return this;
  }

  public LiveServerHandlerConfiguration topicSelector(MessagePublisherTopicSelector topicSelector) {
    this.topicSelector = topicSelector;
    return this;
  }

  public LiveServerHandlerConfiguration liveServerQAStorage(
      LiveServerSubscriptionsQAStorage liveServerQAStorage) {
    this.lsQAStorage = liveServerQAStorage;
    return this;
  }

  public LiveServerHandlerConfiguration jsonMapper(JsonMapper jsonMapper) {
    this.jsonMapper = jsonMapper;
    return this;
  }

  public LiveServerHandlerConfiguration expireAfterWrite(long subscriptionExpire) {
    this.expireAfterWrite = subscriptionExpire;
    return this;
  }

  public LiveServerMessageHandler build() {
    LiveServerMessageHandler handler =
        new LiveServerMessageHandler(
            messagePublisher, topicSelector, lsQAStorage, expireAfterWrite, 10000);
    handler.setClientId(-1);
    handler.setJsonMapper(jsonMapper);
    return handler;
  }
}
