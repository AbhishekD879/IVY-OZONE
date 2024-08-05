package com.entain.oxygen.betbuilder_middleware.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "reactive.redis")
@Data
public class RedissonProperties {

  private String sentinelMaster;

  private String sentinelNodes;

  private String singleHost;

  private int singlePort;

  private boolean isSentinel;

  private String password;
}
