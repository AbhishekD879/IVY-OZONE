package com.coral.oxygen.middleware.featured.configuration;

import com.coral.oxygen.middleware.featured.service.impl.InplayApi;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

@Configuration
public class InplayApiConfiguration {

  private Integer port;
  private String host;

  @Autowired
  public InplayApiConfiguration(
      @Value("${inplay.consumer.host}") String host,
      @Value("${inplay.consumer.port}") Integer port) {
    this.port = port;
    this.host = host;
  }

  @Bean
  public InplayApi getInplayApi() {
    return new Retrofit.Builder()
        .baseUrl(new HttpUrl.Builder().scheme("http").host(host).port(port).build())
        .addConverterFactory(GsonConverterFactory.create())
        .client(new OkHttpClient.Builder().build())
        .build()
        .create(InplayApi.class);
  }
}
