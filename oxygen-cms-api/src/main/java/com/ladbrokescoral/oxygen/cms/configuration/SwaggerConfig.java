package com.ladbrokescoral.oxygen.cms.configuration;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springdoc.core.GroupedOpenApi;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {

  @Value("${springdoc.module-name:CMS API}")
  private String moduleName;

  @Value("${springdoc.api-version:v1.0}")
  private String apiVersion;

  @Bean
  public OpenAPI customOpenAPI() {

    final String securitySchemeName = "bearerAuth";

    return new OpenAPI()
        .addSecurityItem(new SecurityRequirement().addList("bearerAuth"))
        .components(
            new Components()
                .addSecuritySchemes(
                    securitySchemeName,
                    new SecurityScheme()
                        .name(securitySchemeName)
                        .type(SecurityScheme.Type.HTTP)
                        .scheme("bearer")
                        .bearerFormat("JWT")))
        .info(new Info().title(moduleName).version(apiVersion));
  }

  @Bean
  public GroupedOpenApi publicApi() {
    // FXIME: use global property for public path
    return GroupedOpenApi.builder().group("public").pathsToMatch("/cms/api/**").build();
  }

  @Bean
  public GroupedOpenApi privateApi() {
    // FXIME: use global property for private path
    return GroupedOpenApi.builder().group("private").pathsToMatch("/v1/api/**").build();
  }

  @Bean
  public GroupedOpenApi actuatorApi(
      @Value("${management.endpoints.web.base-path}/**") String path) {
    return GroupedOpenApi.builder().group("actuator").pathsToMatch(path).build();
  }
}
