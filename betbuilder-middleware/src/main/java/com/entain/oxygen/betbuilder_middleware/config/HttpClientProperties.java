package com.entain.oxygen.betbuilder_middleware.config;

import lombok.Data;

@Data
public class HttpClientProperties {
  private int tcpKeepIdle;

  private int tcpKeepInterval;

  private int tcpKeepCount;

  private int maxIdleTime;

  private int maxLifeTime;

  private int evictInBackground;

  private int threadMultiplier;

  private int threadKeepAliveSeconds;

  private String connectionName;

  private int maxConnections;
}
