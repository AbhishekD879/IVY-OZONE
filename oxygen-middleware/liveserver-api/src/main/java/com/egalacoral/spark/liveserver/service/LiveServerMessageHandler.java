package com.egalacoral.spark.liveserver.service;

import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisherTopicSelector;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;
import com.egalacoral.spark.liveserver.BaseObjectBuilder;
import com.egalacoral.spark.liveserver.LiveServerListener;
import com.egalacoral.spark.liveserver.Message;
import com.egalacoral.spark.liveserver.meta.EventMetaInfoRepository;
import com.egalacoral.spark.liveserver.utils.JsonMapper;
import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import com.newrelic.api.agent.Trace;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class LiveServerMessageHandler implements LiveServerListener {

  private EventMetaInfoRepository eventMetaInfoRepository;
  private LiveServerSubscriptionsQAStorage lsQAStorage;
  private MessagePublisher messagePublisher;
  private MessagePublisherTopicSelector topicSelector;

  private int clientId;
  private JsonMapper jsonMapper;

  private Cache<String, Integer> messageItems;

  public LiveServerMessageHandler(
      MessagePublisher messagePublisher,
      MessagePublisherTopicSelector topicSelector,
      LiveServerSubscriptionsQAStorage lsQAStorage,
      long expireAfterWrite,
      int maxItemsToStoreSize) {
    this.messagePublisher = messagePublisher;
    this.lsQAStorage = lsQAStorage;
    this.topicSelector = topicSelector;
    this.messageItems =
        CacheBuilder.newBuilder()
            .maximumSize(maxItemsToStoreSize)
            .expireAfterWrite(expireAfterWrite, TimeUnit.SECONDS)
            .recordStats()
            .build();
  }

  public void setEventMetaInfoRepository(EventMetaInfoRepository eventMetaInfoRepository) {
    this.eventMetaInfoRepository = eventMetaInfoRepository;
  }

  @Override
  public void onMessage(Message message) {
    if (message == null) {
      log.error("Empty message.");
      return;
    }
    putToMap(message);
    publish(message);
  }

  @Trace(dispatcher = true, metricName = "LiveServerMessageHandler")
  private void publish(Message message) {
    if (message == null || message.getEvenId() == null) {
      log.error("not data for publishing; message {} ; key is null ;", message);
      return;
    }

    BaseObjectBuilder builder =
        BaseObjectBuilder.create(message, jsonMapper)
            .clientId(clientId)
            .eventMetaInfoRepository(eventMetaInfoRepository);

    String messageJson = builder.toJsonString();
    if (!builder.isValidMessage()) {
      log.warn(
          "Possible configuration error. The message is not valid or event do not exist at LiveServe anymore {} ; key {} ;",
          message.getBody(),
          message.getEvenId());
      return;
    }

    String key = builder.buildMessageKey();

    String cacheKey = builder.buildCacheKey();
    Integer previousHash = messageItems.getIfPresent(cacheKey);
    int thisHash = messageJson.hashCode();
    TopicType topic = topicSelector.getLiveServeMessageTopic();
    if (previousHash == null || previousHash != thisHash) {
      publish(topic, key, messageJson);
      messageItems.put(cacheKey, thisHash);

      if (builder.isScbrdObjectValid()) {
        previousHash = messageItems.getIfPresent(builder.buildScbdCacheKey());
        messageJson = builder.scbrdToJsonString();
        thisHash = messageJson.hashCode();
        if (previousHash == null || previousHash != thisHash) {
          publish(topic, key, messageJson);
          messageItems.put(builder.buildScbdCacheKey(), thisHash);
        }
      }
    } else {
      log.debug("duplicated item # {}", cacheKey);
    }
  }

  private void publish(TopicType topic, String key, String messageJson) {
    messagePublisher.publish(topic, key, messageJson);
    String message = messageJson == null ? null : messageJson.replaceAll("\\n", "");
    log.debug("Publish to ReliableTopic:[{}], message:[{}]", topic, message);
  }

  private void putToMap(Message message) {
    lsQAStorage.storeLiveUpdateMessage(message);
  }

  @Override
  public void onError(Throwable e) {
    // do nothing
  }

  public void setClientId(int clientId) {
    this.clientId = clientId;
  }

  public void setJsonMapper(JsonMapper jsonMapper) {
    this.jsonMapper = jsonMapper;
  }
}
