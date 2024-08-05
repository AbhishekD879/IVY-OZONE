package com.entain.oxygen.promosandbox.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebAppConfig implements WebMvcConfigurer {

  @Value("${management.endpoints.web.cors.allowed-origins}")
  private String corsPaths;

  @Value("${springdoc.swagger-ui.path}")
  private String swaggerUIPath;

  @Override
  public void addCorsMappings(CorsRegistry registry) {
    registry.addMapping("/**").allowedOrigins(corsPaths.split(",")).allowedMethods("*");
  }

  @Override
  public void addViewControllers(ViewControllerRegistry registry) {
    registry.addRedirectViewController("/", swaggerUIPath);
  }
}
