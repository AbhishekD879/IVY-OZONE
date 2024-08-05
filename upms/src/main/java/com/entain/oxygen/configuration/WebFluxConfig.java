package com.entain.oxygen.configuration;

import org.springframework.boot.actuate.autoconfigure.endpoint.web.CorsEndpointProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.config.CorsRegistry;
import org.springframework.web.reactive.config.WebFluxConfigurer;

@Configuration
public class WebFluxConfig implements WebFluxConfigurer {

  private final CorsEndpointProperties corsEndpointProperties;

  public WebFluxConfig(CorsEndpointProperties corsEndpointProperties) {
    this.corsEndpointProperties = corsEndpointProperties;
  }

  @Override
  public void addCorsMappings(CorsRegistry registry) {
    registry
        .addMapping("/**")
        .allowedOrigins(corsEndpointProperties.getAllowedOrigins().toArray(new String[0]))
        .allowedHeaders(corsEndpointProperties.getAllowedHeaders().toArray(new String[0]))
        .allowedMethods(corsEndpointProperties.getAllowedMethods().toArray(new String[0]));
  }
}
