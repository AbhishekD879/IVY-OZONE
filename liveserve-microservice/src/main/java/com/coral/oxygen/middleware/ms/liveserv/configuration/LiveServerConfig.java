package com.coral.oxygen.middleware.ms.liveserv.configuration;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.impl.MessageHandlerMultiplexer;
import com.coral.oxygen.middleware.ms.liveserv.impl.OldEventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.impl.SiteServEventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.impl.kafka.KafkaTopicMessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.newclient.EventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.newclient.SiteServerEventIdResolverAdapter;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.*;
import com.coral.oxygen.middleware.ms.liveserv.qa.QAMessageCollector;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.Proxy.Type;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.Objects;
import java.util.concurrent.TimeUnit;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;
import okhttp3.OkHttpClient;
import okhttp3.OkHttpClient.Builder;
import okhttp3.logging.HttpLoggingInterceptor;
import org.apache.logging.log4j.util.Strings;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class LiveServerConfig {

  @Bean
  public OldEventIdResolver oldEventIdResolver() {
    return new SiteServEventIdResolver();
  }

  @Bean
  public EventIdResolver eventIdResolver(
      OldEventIdResolver oldEventIdResolver,
      @Value("${events.resolved.cache.size}") int sizeOfResolvedEventsCache,
      @Value("${events.resolved.cache.ttl.seconds}") int ttlOfResolvedEventsCache) {
    return new SiteServerEventIdResolverAdapter(
        oldEventIdResolver, sizeOfResolvedEventsCache, ttlOfResolvedEventsCache);
  }

  @Bean
  public MessageHandler multiplexer(
      KafkaTopicMessageHandler kafkaTopicMessageHandler,
      @Autowired(required = false) QAMessageCollector qaMessageCollector) {
    MessageHandlerMultiplexer multiplexer = new MessageHandlerMultiplexer();
    multiplexer.addMessageHandler(kafkaTopicMessageHandler);
    if (qaMessageCollector != null) {
      multiplexer.addMessageHandler(qaMessageCollector);
    }
    return multiplexer;
  }

  @Bean
  public LiveServerListener liveServerListener(
      EventIdResolver eventIdResolver, @Qualifier("multiplexer") MessageHandler messageHandler) {
    return new LiveServerListenerImpl(messageHandler, eventIdResolver);
  }

  /** Client used for long-polling liveserer */
  @Bean
  public OkHttpClient okHttpClient(
      @Value("${liveServer.connection.timeout}") int connectionTimeout,
      @Value("${liveServer.read.timeout}") int readTimeout,
      @Value("${liveServer.logging.level}") String loggingLevel,
      @Value("${http.proxyHost}") String proxyHost,
      @Value("${http.proxyPort}") String proxyPort)
      throws KeyManagementException, NoSuchAlgorithmException {
    HttpLoggingInterceptor interceptor = new HttpLoggingInterceptor();
    interceptor.setLevel(HttpLoggingInterceptor.Level.valueOf(loggingLevel));

    log.warn("**** Allow untrusted SSL connection ****");

    final TrustManager[] listOfTrustManagers =
        new TrustManager[] {
          new X509TrustManager() {
            @Override
            public X509Certificate[] getAcceptedIssuers() {
              return new X509Certificate[0];
            }

            @Override
            public void checkServerTrusted(final X509Certificate[] chain, final String authType)
                throws CertificateException {}

            @Override
            public void checkClientTrusted(final X509Certificate[] chain, final String authType)
                throws CertificateException {}
          }
        };

    SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
    sslContext.init(null, listOfTrustManagers, new java.security.SecureRandom());

    Builder okClientBuilder =
        new Builder()
            .addInterceptor(interceptor)
            .connectionPool(new ConnectionPool(10, 10, TimeUnit.MINUTES))
            .readTimeout(readTimeout, TimeUnit.SECONDS)
            .connectTimeout(connectionTimeout, TimeUnit.SECONDS)
            .sslSocketFactory(
                sslContext.getSocketFactory(), (X509TrustManager) listOfTrustManagers[0])
            .hostnameVerifier(LiveServerConfig::isHostNameVerifier); // Object.nonNull(string)
    if (Strings.isNotBlank(proxyHost) && Strings.isNotBlank(proxyPort)) {
      return okClientBuilder
          .proxy(
              new Proxy(Type.HTTP, new InetSocketAddress(proxyHost, Integer.parseInt(proxyPort))))
          .build();
    }
    return okClientBuilder.build();
  }

  public static boolean isHostNameVerifier(String hostname, SSLSession session) {
    return Objects.nonNull(hostname) && Objects.nonNull(session);
  }

  @Bean
  public Call callExecutor(OkHttpClient okHttpClient) {
    return new LiveServerCall(okHttpClient);
  }

  @Bean
  public LiveServerClientBuilder liveServerClientBuilder(
      @Value("${liveServer.endpoint}") String endpoint, //
      Call call,
      @Value("${liveServer.subscription.expire}") long subscriptionExpire, //
      LiveServerListener liveServerListener) {
    return new LiveServerClientBuilder() //
        .withEndpoint(endpoint) //
        .withCall(call)
        .withSubscriptionExpire(subscriptionExpire)
        .withLiveServerMessageHandler(liveServerListener);
  }
}
