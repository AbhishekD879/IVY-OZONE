package com.oxygen.publisher.configuration;

import com.oxygen.publisher.translator.DiagnosticService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DiagnosticServiceConfig {

  @Bean
  public DiagnosticService diagnosticService() {
    return new DiagnosticService(10 * 1000);
  }
}
