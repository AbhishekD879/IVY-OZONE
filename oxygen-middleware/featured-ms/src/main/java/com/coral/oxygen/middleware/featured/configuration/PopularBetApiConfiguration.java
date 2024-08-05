package com.coral.oxygen.middleware.featured.configuration;

import com.coral.oxygen.middleware.featured.service.impl.PopularBetApi;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

@Configuration
public class PopularBetApiConfiguration {

  private String trendingBetUrl;

  @Autowired
  public PopularBetApiConfiguration(@Value("${trendingbet.url}") String trendingBetUrl) {
    this.trendingBetUrl = trendingBetUrl;
  }

  @Bean
  public PopularBetApi getPopularBetApi() {
    return new Retrofit.Builder()
        .baseUrl(new HttpUrl.Builder().scheme("https").host(trendingBetUrl).build())
        .addConverterFactory(GsonConverterFactory.create())
        .client(new OkHttpClient.Builder().build())
        .build()
        .create(PopularBetApi.class);
  }
}
