package com.ladbrokescoral.oxygen.configuration;

import java.net.URI;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.server.RequestPredicates;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerResponse;

@Configuration
public class WebAppConfig {

  @Value("${management.endpoints.web.base-path}")
  private String actuatorPath;

  @Value("${management.endpoints.web.path-mapping.health}")
  private String healthPath;

  @Value("${management.endpoints.web.path-mapping.info}")
  private String infoPath;

  @Bean
  public RouterFunction<ServerResponse> swaggerRouter() {
    // FIXME: redirect for springdoc-openapi in future
    URI uri = URI.create(actuatorPath);
    return RouterFunctions.route(
        RequestPredicates.GET("/"), req -> ServerResponse.temporaryRedirect(uri).build());
  }

  @Bean
  public RouterFunction<ServerResponse> healthRouter() {
    URI uri = URI.create(actuatorPath + healthPath);
    return RouterFunctions.route(
        RequestPredicates.GET(healthPath), req -> ServerResponse.temporaryRedirect(uri).build());
  }

  @Bean
  public RouterFunction<ServerResponse> infoRouter() {
    URI uri = URI.create(actuatorPath + infoPath);
    return RouterFunctions.route(
        RequestPredicates.GET(infoPath), req -> ServerResponse.temporaryRedirect(uri).build());
  }
}
