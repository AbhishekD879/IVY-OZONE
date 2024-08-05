package com.ladbrokescoral.oxygen.hydra;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebAppConfig implements WebMvcConfigurer {

  @Value("${management.endpoints.web.base-path}")
  private String actuatorPath;

  @Value("${management.endpoints.web.path-mapping.health}")
  private String healthPath;

  @Value("${management.endpoints.web.path-mapping.info}")
  private String infoPath;

  @Override
  public void addViewControllers(ViewControllerRegistry registry) {
    registry.addRedirectViewController("/", actuatorPath);
    registry.addRedirectViewController(healthPath, actuatorPath + healthPath);
    registry.addRedirectViewController(infoPath, actuatorPath + infoPath);
  }
}
