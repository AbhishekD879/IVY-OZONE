package com.ladbrokescoral.oxygen.questionengine.configuration;

import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

import org.springframework.cloud.openfeign.FeignFormatterRegistrar;
import org.springframework.context.annotation.Bean;

import com.ladbrokescoral.oxygen.questionengine.configuration.feign.bpp.BppErrorDecoder;

import feign.codec.ErrorDecoder;

public class BppFeignConfig {

  @Bean
  public ErrorDecoder errorDecoder() {
    return new BppErrorDecoder();
  }

  @Bean
  public FeignFormatterRegistrar feignFormatterRegistrar() {
    return formatterRegistry -> formatterRegistry.addConverter(
        Instant.class,
        String.class,
        source -> DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.of("UTC")).format(source)
    );
  }
}
