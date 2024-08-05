package com.ladbrokescoral.oxygen.cms.configuration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.autoconfigure.endpoint.web.CorsEndpointProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Profile({"!UNIT", "SECURITY"})
@Configuration
public class CorsConfig implements WebMvcConfigurer {

  @Autowired private CorsEndpointProperties corsEndpointProperties;

  @Override
  public void addCorsMappings(CorsRegistry registry) {

    registry
        .addMapping("/**")
        .allowedOrigins(corsEndpointProperties.getAllowedOrigins().toArray(new String[0]))
        .allowedHeaders(corsEndpointProperties.getAllowedHeaders().toArray(new String[0]))
        .allowedMethods(corsEndpointProperties.getAllowedMethods().toArray(new String[0]))
        .exposedHeaders(corsEndpointProperties.getExposedHeaders().toArray(new String[0]))
        .allowCredentials(corsEndpointProperties.getAllowCredentials())
        .maxAge(corsEndpointProperties.getMaxAge().getSeconds());
  }
}
