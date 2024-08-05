package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import java.util.Objects;
import java.util.UUID;
import okhttp3.logging.HttpLoggingInterceptor;

/** Created by Aliaksei Yarotski on 11/7/17. */
public class LiveServerClientBuilder {

  private LiveServerListener liveServerMessageHandler;
  private String endpoint;
  private int connectionTimeout;
  private int readTimeout;
  private long subscriptionExpire;
  private HttpLoggingInterceptor.Level loggingLevel = HttpLoggingInterceptor.Level.BASIC;
  private Call call;

  public LiveServerClientBuilder withEndpoint(String endpoint) {
    this.endpoint = endpoint;
    return this;
  }

  public LiveServerClientBuilder withConnectionTimeout(int connectionTimeout) {
    this.connectionTimeout = connectionTimeout;
    return this;
  }

  public LiveServerClientBuilder withReadTimeout(int readTimeout) {
    this.readTimeout = readTimeout;
    return this;
  }

  public LiveServerClientBuilder withSubscriptionExpire(long subscriptionExpire) {
    this.subscriptionExpire = subscriptionExpire;
    return this;
  }

  public LiveServerClientBuilder withLiveServerMessageHandler(
      LiveServerListener liveServerMessageHandler) {
    this.liveServerMessageHandler = liveServerMessageHandler;
    return this;
  }

  public LiveServerClientBuilder withLoggingLevel(HttpLoggingInterceptor.Level loggingLevel) {
    this.loggingLevel = loggingLevel;
    return this;
  }

  public LiveServerClientBuilder withCall(Call call) {
    this.call = call;
    return this;
  }

  public long getExpireAfterWrite() {
    return subscriptionExpire;
  }

  public LiveServerClient build() {
    return build(UUID.randomUUID().toString());
  }

  public LiveServerClient build(String id) {
    Objects.requireNonNull(liveServerMessageHandler);
    Objects.requireNonNull(endpoint);
    Objects.requireNonNull(call);

    return new LiveServerClient(endpoint, subscriptionExpire, liveServerMessageHandler, id, call);
  }
}
