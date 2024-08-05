package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.ladbrokescoral.oxygen.questionengine.Application;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.SiteServerProperties;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.repository.AwardFailureRepository;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractDataSource;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.socialsignin.spring.data.dynamodb.repository.config.EnableDynamoDBRepositories;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.*;

/**
 * Global config for Question Engine app.
 */
@Configuration
@EnableRetry
@EnableAsync
@EnableAspectJAutoProxy
@EnableScheduling
@EnableSwagger2
@EnableWebMvc
@EnableCaching
@EnableDynamoDBRepositories(basePackageClasses = {UserAnswerRepository.class, AwardFailureRepository.class})
@EnableFeignClients(basePackageClasses = Application.class)
@RequiredArgsConstructor
public class QuestionEngineConfig {
  private final SiteServerProperties siteServerProperties;

  @Bean
  public static ModelMapper modelMapper() {
    return ModelMapperFactory.getInstance();
  }

  @Bean
  public ObjectMapper objectMapper() {
    return ObjectMapperFactory.getInstance().disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }

  @Bean
  public SiteServerApi siteServerAPI() throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder()
        .setUrl(siteServerProperties.getBaseUrl())
        .setLoggingLevel(SiteServerApi.Level.valueOf(siteServerProperties.getLoggingLevel()))
        .setConnectionTimeout(siteServerProperties.getConnectionTimeout())
        .setReadTimeout(siteServerProperties.getReadTimeout())
        .setMaxNumberOfRetries(siteServerProperties.getRetriesNumber())
        .setVersion(siteServerProperties.getApiVersion())
        .build();
  }

  @Bean
  public  Map<String, AbstractDataSource<Quiz>> quizzesMap (){
    return new HashMap<>();
  }

  @Bean
  public  List<Quiz> allPriviousQuizes(){
    return new ArrayList<>();
  }

}
