package com.ladbrokescoral.oxygen.buildyourbetms.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.autoconfigure.endpoint.web.CorsEndpointProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.config.CorsRegistry;
import org.springframework.web.reactive.config.WebFluxConfigurer;
import org.springframework.web.reactive.config.WebFluxConfigurerComposite;
import org.springframework.web.reactive.function.server.RequestPredicates;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerResponse;

@Configuration
public class WebAppConfig {

  @Bean
  public RouterFunction<ServerResponse> docsContent(
      @Value("classpath:/static/docs/index.html") Resource html) {
    // FIXME: redirect for springdoc-openapi in future
    return RouterFunctions.route(
        RequestPredicates.GET("/"),
        request -> ServerResponse.ok().contentType(MediaType.TEXT_HTML).bodyValue(html));
  }

  @Bean
  public WebFluxConfigurer corsConfigurer(CorsEndpointProperties corsEndpointProperties) {
    return new WebFluxConfigurerComposite() {
      @Override
      public void addCorsMappings(CorsRegistry registry) {
        registry
            .addMapping("/api/**")
            .allowedOrigins(
                corsEndpointProperties.getAllowedOrigins().stream().toArray(String[]::new))
            .allowedMethods(
                corsEndpointProperties.getAllowedMethods().stream().toArray(String[]::new));
      }
    };
  }
}
