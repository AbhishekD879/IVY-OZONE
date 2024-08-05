package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.service.showdown.ShowdownEndPoint;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;
import okhttp3.OkHttpClient;
import okhttp3.OkHttpClient.Builder;
import okhttp3.logging.HttpLoggingInterceptor;
import okhttp3.logging.HttpLoggingInterceptor.Logger;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

@Slf4j
@Configuration
public class ShowdownClientConfig {
  @Bean
  public OkHttpClient showdownOkHttpClient(
      @Value("${showdown.timout.read:10000}") int readTimeout,
      @Value("${showdown.timout.connect:3000}") int connectTimeout,
      @Value("${showdown.logging.level:BASIC}") String showdownLoggingLevel,
      @Value("${showdown.max-idle-connections:5}") int showdownMaxIdleConnections,
      @Value("${showdown.keep-alive-duration.level:60000}") int showdownKeepAliveDuration) {
    Logger logger = log::info;
    HttpLoggingInterceptor interceptor = new HttpLoggingInterceptor(logger);
    interceptor.setLevel(HttpLoggingInterceptor.Level.valueOf(showdownLoggingLevel));
    log.info("Showdown client logging level : {}", showdownLoggingLevel);

    Builder clientBuilder =
        new Builder()
            .addInterceptor(interceptor)
            .addInterceptor(interceptor)
            .connectionPool(
                new ConnectionPool(
                    showdownMaxIdleConnections, showdownKeepAliveDuration, TimeUnit.MILLISECONDS))
            .readTimeout(readTimeout, TimeUnit.MILLISECONDS)
            .connectTimeout(connectTimeout, TimeUnit.MILLISECONDS);

    return clientBuilder.build();
  }

  @Bean
  public ShowdownEndPoint showdownEndPoint(
      @Value("${showdown.base.url}") String baseUrl,
      @Qualifier("showdownOkHttpClient") OkHttpClient showdownOkHttpClient) {
    return new Retrofit.Builder()
        .baseUrl(baseUrl)
        .client(showdownOkHttpClient)
        .addConverterFactory(JacksonConverterFactory.create())
        .build()
        .create(ShowdownEndPoint.class);
  }
}
