package com.entain.oxygen.betbuilder_middleware.config;

import lombok.Data;

@Data
public class WebClientProperties extends HttpClientProperties {

  private String baseUrl;

  private int maxInMemorySize;

  private boolean keepAlive;

  private int connectionTimeoutMillis;

  private boolean useEpoll;

  private long readTimeoutMillis;

  private long writeTimeoutMillis;

  private String threadNamePrefix;

  private int numberOfThreads;

  private String contentType;

  private boolean compressionEnabled;

  private boolean useGlobalResources;

  private boolean wiretapEnabled;

  private int pendingAcquireMaxCount;

  private int pendingAcquireTimeout;
}
