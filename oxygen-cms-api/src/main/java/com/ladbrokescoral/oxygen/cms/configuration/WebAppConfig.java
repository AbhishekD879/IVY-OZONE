package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.format.FormatterRegistry;
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

  @Value("${springdoc.swagger-ui.path}")
  private String swaggerUIPath;

  @Override
  public void addViewControllers(ViewControllerRegistry registry) {
    registry.addRedirectViewController("/", swaggerUIPath);
    registry.addRedirectViewController(healthPath, actuatorPath + healthPath);
    registry.addRedirectViewController(infoPath, actuatorPath + infoPath);
  }

  /** We may want to support lowercase letters in the request URL. */
  @Override
  public void addFormatters(FormatterRegistry registry) {
    registry.addConverter(new FileTypeConverter());
  }

  private static final class FileTypeConverter implements Converter<String, FileType> {
    @Override
    public FileType convert(String source) {
      return FileType.valueOf(source.toUpperCase());
    }
  }
}
