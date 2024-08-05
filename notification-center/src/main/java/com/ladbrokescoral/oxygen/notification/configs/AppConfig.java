package com.ladbrokescoral.oxygen.notification.configs;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.client.LiveServerCall;
import com.coral.oxygen.middleware.ms.liveserv.client.RetryableCall;
import com.coral.oxygen.middleware.ms.liveserv.impl.EventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.impl.SiteServEventIdResolver;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fortify.annotations.FortifyValidate;
import com.fortify.annotations.FortifyXSSValidate;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.ladbrokescoral.oxygen.notification.client.optin.IGameMediaApi;
import com.ladbrokescoral.oxygen.notification.entities.dto.RacingDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.WinAlertDTO;
import com.ladbrokescoral.oxygen.notification.services.ChannelMessageListener;
import com.ladbrokescoral.oxygen.notification.services.NotificationsMessageHandler;
import com.ladbrokescoral.oxygen.notification.utils.exceptions.BetTypesMapException;
import com.ladbrokescoral.scoreboards.parser.api.BipParser;
import com.ladbrokescoral.scoreboards.parser.api.BipParserFactory;
import com.ladbrokescoral.scoreboards.parser.model.EventCategory;
import io.vavr.jackson.datatype.VavrModule;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.support.ReloadableResourceBundleMessageSource;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisKeyValueAdapter;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.listener.PatternTopic;
import org.springframework.data.redis.listener.RedisMessageListenerContainer;
import org.springframework.data.redis.listener.adapter.MessageListenerAdapter;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;
import org.springframework.scheduling.annotation.EnableScheduling;

@Slf4j
@Configuration
@EnableScheduling
@EnableRedisRepositories(
    basePackages = {"com.ladbrokescoral.oxygen.notification"},
    enableKeyspaceEvents = RedisKeyValueAdapter.EnableKeyspaceEvents.ON_STARTUP,
    keyspaceNotificationsConfigParameter = "")
public class AppConfig {

  @Bean
  public ScheduledExecutorService scheduledPool(
      @Value("${liveserv.message-listener.scheduled-pool-core-size}") int corePoolSize) {
    return Executors.newScheduledThreadPool(corePoolSize);
  }

  @Bean(name = "messageSource")
  public ReloadableResourceBundleMessageSource messageSource() {
    final ReloadableResourceBundleMessageSource messageBundle =
        new ReloadableResourceBundleMessageSource();
    messageBundle.setBasename("classpath:messages/messages");
    messageBundle.setDefaultEncoding("UTF-8");
    return messageBundle;
  }

  @Bean
  Gson gson() {
    return new GsonBuilder().create();
  }

  @Bean
  Map<String, String> betTypesMap(Gson gson) {
    Type stringMapType = new TypeToken<Map<String, String>>() {}.getType();
    try (InputStreamReader betTypesStream =
        new InputStreamReader(
            this.getClass().getClassLoader().getResourceAsStream("map/bet_types_map.json"))) {
      return gson.fromJson(betTypesStream, stringMapType);
    } catch (IOException e) {
      throw new BetTypesMapException("betTypesMap is not initialized", e);
    }
  }

  @Bean
  @FortifyXSSValidate
  @FortifyValidate("return")
  RedisTemplate<String, WinAlertDTO> winAlertDTORedisTemplate(RedisConnectionFactory factory) {
    RedisTemplate<String, WinAlertDTO> redisTemplate = new RedisTemplate<>();
    Jackson2JsonRedisSerializer<WinAlertDTO> jackson2JsonRedisSerializer =
        new Jackson2JsonRedisSerializer<>(WinAlertDTO.class);
    jackson2JsonRedisSerializer.setObjectMapper(
        new ObjectMapper().registerModule(new VavrModule()));
    RedisSerializer<String> stringRedisSerializer = new StringRedisSerializer();
    redisTemplate.setConnectionFactory(factory);
    redisTemplate.setKeySerializer(stringRedisSerializer);
    redisTemplate.setValueSerializer(jackson2JsonRedisSerializer);
    redisTemplate.setHashKeySerializer(stringRedisSerializer);
    redisTemplate.setHashValueSerializer(jackson2JsonRedisSerializer);
    redisTemplate.afterPropertiesSet();
    return redisTemplate;
  }

  @Bean
  @FortifyXSSValidate
  @FortifyValidate("return")
  RedisTemplate<String, List<String>> winAlertSubScriptionRedisTemplate(
      RedisConnectionFactory factory) {
    RedisTemplate<String, List<String>> redisTemplate = new RedisTemplate<>();
    Jackson2JsonRedisSerializer<?> jackson2JsonRedisSerializer =
        new Jackson2JsonRedisSerializer<>(ArrayList.class);
    jackson2JsonRedisSerializer.setObjectMapper(
        new ObjectMapper().registerModule(new VavrModule()));
    RedisSerializer<String> stringRedisSerializer = new StringRedisSerializer();
    redisTemplate.setConnectionFactory(factory);
    redisTemplate.setKeySerializer(stringRedisSerializer);
    redisTemplate.setValueSerializer(jackson2JsonRedisSerializer);
    redisTemplate.setHashKeySerializer(stringRedisSerializer);
    redisTemplate.setHashValueSerializer(jackson2JsonRedisSerializer);
    redisTemplate.afterPropertiesSet();
    return redisTemplate;
  }

  @Bean
  @FortifyXSSValidate
  RedisTemplate<String, RacingDTO> racingDTORedisTemplate(RedisConnectionFactory factory) {
    RedisTemplate<String, RacingDTO> redisTemplate = new RedisTemplate<>();
    Jackson2JsonRedisSerializer<RacingDTO> jackson2JsonRedisSerializer =
        new Jackson2JsonRedisSerializer<>(RacingDTO.class);
    RedisSerializer<String> stringRedisSerializer = new StringRedisSerializer();
    jackson2JsonRedisSerializer.setObjectMapper(
        new ObjectMapper().registerModule(new VavrModule()));
    redisTemplate.setConnectionFactory(factory);
    redisTemplate.setKeySerializer(stringRedisSerializer);
    redisTemplate.setValueSerializer(jackson2JsonRedisSerializer);
    redisTemplate.setHashKeySerializer(stringRedisSerializer);
    redisTemplate.setHashValueSerializer(jackson2JsonRedisSerializer);
    redisTemplate.afterPropertiesSet();
    return redisTemplate;
  }

  @Qualifier("StringRedisTemplate")
  @Bean
  StringRedisTemplate template(RedisConnectionFactory connectionFactory) {
    StringRedisTemplate redisTemplate = new StringRedisTemplate();
    RedisSerializer<String> stringRedisSerializer = new StringRedisSerializer();
    redisTemplate.setConnectionFactory(connectionFactory);
    redisTemplate.setKeySerializer(stringRedisSerializer);
    redisTemplate.setValueSerializer(stringRedisSerializer);
    redisTemplate.setHashKeySerializer(stringRedisSerializer);
    redisTemplate.setHashValueSerializer(stringRedisSerializer);
    redisTemplate.afterPropertiesSet();
    return redisTemplate;
  }

  @Bean
  public SiteServerApi siteServerAPI(
      @Value("${siteServer.base.url}") String siteServerUrl,
      @Value("${siteServer.api.version}") String apiVersion,
      @Value("${siteServer.connection.timeout}") int connectionTimeout,
      @Value("${siteServer.read.timeout}") int readTimeout,
      @Value("${siteServer.retries.number}") int retriesNumber,
      @Value("${siteServer.logging.level}") String loggingLevel)
      throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder()
        .setUrl(siteServerUrl)
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setMaxNumberOfRetries(retriesNumber)
        .setVersion(apiVersion)
        .build();
  }

  @Bean
  public IGameMediaApi iGameMediaApi(
      @Value("${oxygen-settings.base.url}") String iGameApiUrl,
      @Value("${oxygen-settings.connection.timeout}") int connectionTimeout,
      @Value("${oxygen-settings.read.timeout}") int readTimeout,
      @Value("${oxygen-settings.retries.number}") int retriesNumber,
      @Value("${oxygen-settings.logging.level}") String loggingLevel)
      throws NoSuchAlgorithmException, KeyManagementException {
    return new IGameMediaApi.Builder()
        .setUrl(iGameApiUrl)
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setMaxNumberOfRetries(retriesNumber)
        .build();
  }

  @Bean
  public SiteServEventIdResolver siteServEventIdResolver(SiteServerApi siteServerAPI) {
    return new SiteServEventIdResolver(siteServerAPI);
  }

  @Bean
  public Call call(
      @Value("${liveserv.url}") String url,
      @Value("${liveserv.timeout.connection}") long connectionTimeout,
      @Value("${liveserv.timeout.read}") long readTimeout,
      @Value("${retries.count}") int retriesCount,
      @Value("${sleep.after.error.time}") long retriesDelay) {
    Call call;
    try {
      call = new LiveServerCall(url, connectionTimeout, readTimeout);
    } catch (NoSuchAlgorithmException | KeyManagementException e) {
      String errorMsg = "Failed to construct LiveServerCall";
      logger.error(errorMsg, e);
      throw new RuntimeException(errorMsg);
    }
    RetryableCall retrievableCall = new RetryableCall(call);
    retrievableCall.setRetriesCount(retriesCount);
    retrievableCall.setRetriesDelay(retriesDelay);
    return retrievableCall;
  }

  @Bean
  RedisMessageListenerContainer container(RedisConnectionFactory connectionFactory) {
    RedisMessageListenerContainer container = new RedisMessageListenerContainer();
    container.setConnectionFactory(connectionFactory);
    return container;
  }

  @Bean
  public LiveServService liveServService(
      Call call,
      EventIdResolver resolver,
      RedisMessageListenerContainer container,
      NotificationsMessageHandler messageHandler,
      ScheduledExecutorService scheduledPool) {
    LiveServService liveServService = new LiveServService(call, messageHandler, resolver);

    ChannelMessageListener channelMessageListener = new ChannelMessageListener();
    channelMessageListener.setLiveService(liveServService);
    MessageListenerAdapter adapter = new MessageListenerAdapter(channelMessageListener);

    container.addMessageListener(adapter, new PatternTopic("channel"));
    container.addMessageListener(
        (message, pattern) -> {
          logger.warn("Application will be restarted");
          scheduledPool.scheduleWithFixedDelay(
              () -> Runtime.getRuntime().exit(-1), 5, 5, TimeUnit.SECONDS);
        },
        new PatternTopic("system"));
    liveServService.startConsuming();
    return liveServService;
  }

  @Bean
  public BipParser footballBipParser() {
    return BipParserFactory.getParser(EventCategory.FOOTBALL);
  }
}
