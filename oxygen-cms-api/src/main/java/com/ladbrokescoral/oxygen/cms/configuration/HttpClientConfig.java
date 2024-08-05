package com.ladbrokescoral.oxygen.cms.configuration;

import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;
import okhttp3.OkHttpClient;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
public class HttpClientConfig {

  @Bean
  public CloseableHttpClient httpClient() {
    return HttpClientBuilder.create().build();
  }

  @Bean
  public OkHttpClient okHttpClient(
      @Value("${ok.http.pool.idle.count}") int idleConnections,
      @Value("${ok.http.pool.idle.ttl.seconds}") long keepAliveSeconds) {
    return new OkHttpClient.Builder()
        .connectionPool(new ConnectionPool(idleConnections, keepAliveSeconds, TimeUnit.SECONDS))
        .retryOnConnectionFailure(false)
        .build();
  }
}
