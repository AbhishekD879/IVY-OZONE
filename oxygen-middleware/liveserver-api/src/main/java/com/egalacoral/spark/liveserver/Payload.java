package com.egalacoral.spark.liveserver;

import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import java.util.List;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class Payload {
  private Cache<String, SubscriptionSubject> payloadItems;

  public Payload(long expireAfterWrite) {
    super();
    payloadItems =
        CacheBuilder.newBuilder()
            .maximumSize(10000)
            .expireAfterWrite(expireAfterWrite, TimeUnit.SECONDS)
            .recordStats()
            .build();
  }

  public void invalidate(String key) {
    this.payloadItems.invalidate(key);
  }

  public SubscriptionSubject addItem(SubscriptionSubject item) {
    SubscriptionSubject savedItem = payloadItems.getIfPresent(item.messageHashKey());
    if (savedItem == null) {
      payloadItems.put(item.messageHashKey(), item);
      savedItem = item;
    }
    return savedItem;
  }

  public void clear() {
    payloadItems.cleanUp();
  }

  /**
   * Updates {@link SubscriptionSubject#lastMessageID} for items that currently exist in cache
   *
   * @param messages - liveserv messages
   */
  public void update(List<Message> messages) {
    for (Message message : messages) {
      String key = message.getEventHash();
      SubscriptionSubject item = payloadItems.getIfPresent(key);
      String lastMessageID = message.getLastMessageID();

      if (item != null) {
        item.addLastMessageID(lastMessageID);
        payloadItems.put(key, item);
      } else {
        log.info(
            "Item {} not found in cache. Skipping last message id update: {}", key, lastMessageID);
      }
    }
  }

  public ConcurrentMap<String, SubscriptionSubject> getPayloadItems() {
    return payloadItems.asMap();
  }
}
