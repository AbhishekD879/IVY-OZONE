package com.entain.oxygen.betbuilder_middleware.exception;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "error")
@Data
public class ErrorStatus {

  private String status2;
  private String status3;
  private String status4;
  private String status5;
  private String status6;
}
