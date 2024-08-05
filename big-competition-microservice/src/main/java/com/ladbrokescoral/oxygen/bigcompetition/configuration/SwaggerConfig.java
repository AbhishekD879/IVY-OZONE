package com.ladbrokescoral.oxygen.bigcompetition.configuration;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springdoc.core.GroupedOpenApi;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {

  @Value("${springdoc.module-name:competition}")
  private String moduleName;

  @Value("${springdoc.api-version:v1.0}")
  private String apiVersion;

  @Value("${management.endpoints.web.base-path}/**")
  private String path;

  @Bean
  public OpenAPI customOpenApi() {
    return new OpenAPI().info(new Info().title(moduleName).version(apiVersion));
  }

  @Bean
  public GroupedOpenApi publicApi() {
    return GroupedOpenApi.builder().group("public").pathsToMatch("/competition/**").build();
  }

  @Bean
  public GroupedOpenApi actuatorApi() {
    return GroupedOpenApi.builder().group("actuator").pathsToMatch(path).build();
  }
}
