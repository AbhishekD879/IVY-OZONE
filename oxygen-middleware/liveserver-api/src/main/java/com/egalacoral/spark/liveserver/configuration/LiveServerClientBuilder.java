package com.egalacoral.spark.liveserver.configuration;

import com.egalacoral.spark.liveserver.Call;
import com.egalacoral.spark.liveserver.LiveServerClient;
import com.egalacoral.spark.liveserver.LiveServerListener;
import com.egalacoral.spark.liveserver.meta.EventMetaInfoRepository;
import java.util.UUID;

/** Created by Aliaksei Yarotski on 11/7/17. */
public class LiveServerClientBuilder {

  private LiveServerListener liveServerMessageHandler;
  private String endpoint;
  private long subscriptionExpire;
  private Call call;

  public LiveServerClientBuilder endpoint(String endpoint) {
    this.endpoint = endpoint;
    return this;
  }

  public LiveServerClientBuilder subscriptionExpire(long subscriptionExpire) {
    this.subscriptionExpire = subscriptionExpire;
    return this;
  }

  public LiveServerClientBuilder liveServerMessageHandler(
      LiveServerListener liveServerMessageHandler) {
    this.liveServerMessageHandler = liveServerMessageHandler;
    return this;
  }

  public LiveServerClientBuilder call(Call call) {
    this.call = call;
    return this;
  }

  public long getExpireAfterWrite() {
    return subscriptionExpire;
  }

  public LiveServerClient build(EventMetaInfoRepository eventMetaInfoRepository) {
    return build(UUID.randomUUID().toString(), eventMetaInfoRepository);
  }

  public LiveServerClient build(String id, EventMetaInfoRepository eventMetaInfoRepository) {
    return new LiveServerClient(
        endpoint, call, subscriptionExpire, liveServerMessageHandler, eventMetaInfoRepository, id);
  }
}
