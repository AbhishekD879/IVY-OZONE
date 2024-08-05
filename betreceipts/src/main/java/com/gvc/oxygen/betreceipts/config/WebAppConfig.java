package com.gvc.oxygen.betreceipts.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebAppConfig implements WebMvcConfigurer {

  @Value("${springdoc.swagger-ui.path}")
  private String swaggerUIPath;

  @Value("${management.endpoints.web.cors.allowed-origins}")
  private String corsPaths;

  @Override
  public void addViewControllers(ViewControllerRegistry registry) {
    registry.addRedirectViewController("/", swaggerUIPath);
  }

  @Override
  public void addCorsMappings(CorsRegistry registry) {

    registry.addMapping("/**").allowedOrigins(corsPaths.split(",")).allowedMethods("*");
  }
}
