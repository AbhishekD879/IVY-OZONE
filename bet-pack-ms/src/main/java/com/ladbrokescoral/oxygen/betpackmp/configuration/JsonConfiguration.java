package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class JsonConfiguration {

  @Bean
  public Gson gsonInstance() {
    return new GsonBuilder().serializeNulls().create();
  }
}
