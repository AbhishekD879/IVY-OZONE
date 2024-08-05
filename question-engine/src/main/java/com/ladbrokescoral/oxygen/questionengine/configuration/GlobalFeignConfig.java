package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.exception.ThirdPartyException;
import feign.Logger;
import feign.codec.Decoder;
import feign.optionals.OptionalDecoder;
import org.springframework.boot.autoconfigure.http.HttpMessageConverters;
import org.springframework.cloud.openfeign.support.SpringDecoder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;

@Configuration
public class GlobalFeignConfig {

  @Bean
  public Decoder optionalAwareSpringFeignDecoder() {
    Decoder delegate = new SpringDecoder(() -> new HttpMessageConverters(new MappingJackson2HttpMessageConverter(feignObjectMapper())));
    OptionalDecoder optionalDecoder = new OptionalDecoder(delegate);

    return (response, type) -> {
      try {
        return optionalDecoder.decode(response, type);
      } catch (Exception ex) {
        throw new ThirdPartyException(String.format("Error while calling third party service. Status: '%s', Reason: '%s'",
            response.status(),
            response.reason()),
            ex);
      }
    };
  }

  @Bean
  public Logger.Level feignLoggerLevel() {
    return Logger.Level.BASIC;
  }

  private ObjectMapper feignObjectMapper() {
    return ObjectMapperFactory.getInstance().disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
  }
}
