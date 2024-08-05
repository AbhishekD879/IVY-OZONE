package com.entain.oxygen.bpp;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "bpp.light")
@Data
public class BppConfigLightProps implements BppProperties {

  private int retryNumber;

  private int retryTimeout;

  private int connectTimeout;

  private int readTimeout;

  private int writeTimeout;

  private int poolSize;

  private int threads;

  private boolean keepAlive;
}
