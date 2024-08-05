package com.egalacoral.spark.liveserver.configuration;

import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisherTopicSelector;
import com.egalacoral.spark.liveserver.Call;
import com.egalacoral.spark.liveserver.LiveServerCall;
import com.egalacoral.spark.liveserver.meta.EventMetaCachedRepoImpl;
import com.egalacoral.spark.liveserver.meta.EventMetaInfoCachedRepository;
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage;
import com.egalacoral.spark.liveserver.utils.JsonMapper;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.time.Duration;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j(topic = "LiveServeOkHttp")
@Configuration
public class LiveServerConfiguration {

  public static final int MAX_IDLE_CONNECTIONS = 10;
  public static final long KEEP_ALIVE_DURATION = 10L;

  @Bean
  public EventMetaInfoCachedRepository eventMetaInfoCachedRepository() {
    return new EventMetaCachedRepoImpl(
        Caffeine.newBuilder().expireAfterAccess(Duration.ofHours(1)).build());
  }

  /** Client used for long-polling liveserver */
  @Bean
  public OkHttpClient liveServeOkHttpClient(
      @Value("${liveServer.connection.timeout}") long connectionTimeout,
      @Value("${liveServer.read.timeout}") long readTimeout,
      @Value("${liveServer.logging.level}") String loggingLevel,
      OkHttpClientCreator okHttpClientCreator,
      @Value("${http.proxyHost}") String proxyHost,
      @Value("${http.proxyPort}") String proxyPort)
      throws KeyManagementException, NoSuchAlgorithmException {
    return okHttpClientCreator.createOkHttpClient(
        connectionTimeout,
        readTimeout,
        MAX_IDLE_CONNECTIONS,
        KEEP_ALIVE_DURATION,
        log::info,
        loggingLevel,
        proxyHost,
        proxyPort);
  }

  @Bean
  public Call callExecutor(@Qualifier("liveServeOkHttpClient") OkHttpClient okHttpClient) {
    return new LiveServerCall(okHttpClient);
  }

  /**
   * Builder for multiply live clients with single tone hazelcast and ls. message handlers.
   *
   * @param endpoint liveServer endpoint.
   * @param call implementation of {@link Call} that executes long-polling requests
   * @param subscriptionExpire liveServer subscription expire.
   * @param jsonMapper wrapper for faster xml jackson ObjectMapper
   * @return LiveServerClientBuilder to build LiveServerClient
   */
  @Bean
  public LiveServerClientBuilder liveServerClientBuilder(
      @Value("${liveServer.endpoint}") String endpoint,
      Call call,
      @Value("${liveServer.subscription.expire}") long subscriptionExpire,
      LiveServerSubscriptionsQAStorage lsQAStorage,
      MessagePublisher messagePublisher,
      MessagePublisherTopicSelector topicSelector,
      JsonMapper jsonMapper) {

    return new LiveServerClientBuilder()
        .endpoint(endpoint)
        .call(call)
        .subscriptionExpire(subscriptionExpire)
        .liveServerMessageHandler(
            new LiveServerHandlerConfiguration()
                .liveServerQAStorage(lsQAStorage)
                .messagePublisher(messagePublisher)
                .topicSelector(topicSelector)
                .expireAfterWrite(subscriptionExpire)
                .jsonMapper(jsonMapper)
                .build());
  }
}
