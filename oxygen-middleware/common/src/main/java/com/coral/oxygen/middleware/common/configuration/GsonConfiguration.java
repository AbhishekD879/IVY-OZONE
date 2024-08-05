package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.JsonFacade;
import com.google.gson.Gson;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GsonConfiguration {

  @Bean
  public Gson getGson() {
    return JsonFacade.GSON;
  }
}
