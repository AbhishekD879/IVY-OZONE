package com.coral.oxygen.middleware.ms.liveserv.configuration;

import com.coral.oxygen.middleware.ms.liveserv.utils.CustomeTypeAdapter;
import com.coral.siteserver.api.CallsAPI;
import com.coral.siteserver.api.SiteServerService;
import com.fatboyindustrial.gsonjodatime.Converters;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.util.concurrent.TimeUnit;
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/** Created by azayats on 08.05.17. */
@org.springframework.context.annotation.Configuration
@EnableRedisRepositories(basePackages = "com.coral.oxygen.middleware.ms.liveserv")
public class Configuration {

  @Bean
  @Qualifier("distributedPrefix")
  public String distributedPrefix(@Value("${distributed.prefix}") String prefix) {
    return prefix;
  }

  @Bean
  public Gson gson() {
    return new GsonBuilder().registerTypeAdapter(Error.class, new CustomeTypeAdapter()).create();
  }

  @Bean
  public SiteServerService getSiteServerService(
      @Value("${siteServer.base.url}") String baseUrl,
      @Value("${siteServer.api.version}") String apiVersion,
      @Value("${siteServer.logging.level}") String level,
      @Value("${siteServer.connection.timeout}") int connectionTimeout,
      @Value("${siteServer.read.timeout}") int readTimeout,
      @Value("${siteServer.retries.number}") int retriesNumber) {

    Logger logger = LoggerFactory.getLogger(CallsAPI.class);

    HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor(logger::info);
    loggingInterceptor.setLevel(HttpLoggingInterceptor.Level.valueOf(level));

    OkHttpClient httpClient =
        new OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .readTimeout(readTimeout, TimeUnit.SECONDS)
            .connectTimeout(connectionTimeout, TimeUnit.SECONDS)
            .build();

    GsonBuilder gsonBuilder = new GsonBuilder();
    gsonBuilder = gsonBuilder.registerTypeAdapter(Error.class, new CustomeTypeAdapter());
    Retrofit retrofit =
        new Retrofit.Builder()
            .baseUrl(baseUrl)
            .addConverterFactory(
                GsonConverterFactory.create(Converters.registerDateTime(gsonBuilder).create()))
            .client(httpClient)
            .build();

    CallsAPI api = retrofit.create(CallsAPI.class);

    return new SiteServerService(api, apiVersion, retriesNumber);
  }
}
