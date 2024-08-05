package com.oxygen.publisher.sportsfeatured.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.newrelic.api.agent.NewRelic;
import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import okhttp3.HttpUrl;
import okhttp3.Interceptor;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

/** Created by Aliaksei Yarotski on 1/11/18. */
@Slf4j
@RequiredArgsConstructor
@Component
public class FeaturedApiProvider implements ReloadableService {

  private final ObjectMapper objectMapper;
  private final List<Interceptor> interceptors;

  private AtomicReference<FeaturedApi> thisFeaturedApi = new AtomicReference<>();
  private AtomicBoolean isOnService = new AtomicBoolean();

  @Value("${featured.consumer.host}")
  private String featuredConsumerHost;

  @Value("${featured.consumer.port}")
  private Integer featuredConsumerPort;

  public FeaturedApi featuredApi() {
    return thisFeaturedApi.get();
  }

  @Override
  public void start() {
    OkHttpClient.Builder httpClientBuilder = new OkHttpClient.Builder();
    interceptors.forEach(httpClientBuilder::addInterceptor);

    HttpUrl url =
        new HttpUrl.Builder()
            .scheme("http")
            .host(featuredConsumerHost)
            .port(featuredConsumerPort)
            .build();
    thisFeaturedApi.set(
        new Retrofit.Builder()
            .baseUrl(url)
            .addConverterFactory(JacksonConverterFactory.create(objectMapper))
            .client(httpClientBuilder.build())
            .build()
            .create(FeaturedApi.class));
    isOnService.set(true);
    log.info("Started FeaturedApiProvider {}:{}", featuredConsumerHost, featuredConsumerPort);
  }

  @Override
  public void evict() {
    // NA
  }

  @Override
  public boolean isHealthy() {
    return isOnService.get();
  }

  @Override
  public void onFail(Exception ex) {
    log.error("Failed on middleware call.", ex);
    NewRelic.noticeError(ex);
    isOnService.set(false);
  }
}
