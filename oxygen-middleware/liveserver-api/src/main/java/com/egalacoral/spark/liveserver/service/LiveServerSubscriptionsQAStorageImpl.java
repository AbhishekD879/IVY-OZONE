package com.egalacoral.spark.liveserver.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.LIVE_SERVER_MODULE_MAP;
import static com.coral.oxygen.middleware.common.configuration.DistributedKey.LIVE_SERVER_SUBSCRIPTIONS_MAP;
import static java.util.Collections.unmodifiableMap;

import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.imdg.DistributedMap;
import com.egalacoral.spark.liveserver.Message;
import com.egalacoral.spark.liveserver.SubscriptionSubject;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class LiveServerSubscriptionsQAStorageImpl implements LiveServerSubscriptionsQAStorage {
  private DistributedMap<String, Message> liveServerModuleMap;
  private DistributedMap<String, SubscriptionSubject> liveServerSubscriptions;
  private String activeProfile;

  @Autowired
  public LiveServerSubscriptionsQAStorageImpl(
      @Value("${spring.profiles.active}") String activeProfile,
      DistributedInstance distributedInstance) {
    this.liveServerModuleMap = distributedInstance.getMap(LIVE_SERVER_MODULE_MAP);
    this.liveServerSubscriptions = distributedInstance.getMap(LIVE_SERVER_SUBSCRIPTIONS_MAP);
    this.activeProfile = activeProfile;
  }

  @Override
  public void storeActiveLiveServePayload(Map<String, SubscriptionSubject> liveservePayload) {
    executeIfDevProfile(() -> liveServerSubscriptions.putAll(liveservePayload));
  }

  @Override
  public void storeLiveUpdateMessage(Message message) {
    executeIfDevProfile(
        () -> {
          String key = message.getEventHash();
          liveServerModuleMap.put(key, message);
        });
  }

  @Override
  public Map<String, Message> getMessages() {
    return unmodifiableMap(liveServerModuleMap);
  }

  @Override
  public Map<String, SubscriptionSubject> getSubscriptions() {
    return unmodifiableMap(liveServerSubscriptions);
  }

  private void executeIfDevProfile(Runnable runnable) {
    if (activeProfile.contains("DEV")) {
      runnable.run();
    }
  }
}
