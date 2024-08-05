package com.ladbrokescoral.oxygen.notification.client.optin;

import com.egalacoral.spark.siteserver.api.SiteServerImpl;
import com.ladbrokescoral.oxygen.notification.client.optin.model.IGMEvent;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import okhttp3.logging.HttpLoggingInterceptor;

/**
 * Client class for IGameMedia API It is in separate package and designed in a way that it could be
 * moved to library on nexus.
 */
public interface IGameMediaApi {

  /**
   * Provides a list of events, that are currently streaming.
   *
   * @return a list of IGameMedia events
   */
  List<IGMEvent> getOpenedStreamEvents();

  class Builder {
    private Integer maxNumberOfRetries = 2;
    private Integer readTimeout = 10;
    private Integer connectionTimeout = 10;
    private String baseUrl = "https://127.0.0.1";
    private int poolSize = 5;
    private long keepAliveSeconds = 5 * 60;
    private HttpLoggingInterceptor.Level level = HttpLoggingInterceptor.Level.BODY;

    public Builder setUrl(String baseUrl) {
      this.baseUrl = baseUrl;
      return this;
    }

    public Builder setMaxNumberOfRetries(Integer maxNumberOfRetries) {
      this.maxNumberOfRetries = maxNumberOfRetries;
      return this;
    }

    public Builder setReadTimeout(Integer readTimeout) {
      this.readTimeout = readTimeout;
      return this;
    }

    public Builder setConnectionTimeout(Integer connectionTimeout) {
      this.connectionTimeout = connectionTimeout;
      return this;
    }

    public Builder setLoggingLevel(SiteServerImpl.Level level) {
      switch (level) {
        case NONE:
          this.level = HttpLoggingInterceptor.Level.NONE;
          break;
        case BASIC:
          this.level = HttpLoggingInterceptor.Level.BASIC;
          break;
        case HEADERS:
          this.level = HttpLoggingInterceptor.Level.HEADERS;
          break;
        case BODY:
          this.level = HttpLoggingInterceptor.Level.BODY;
          break;
        default:
          this.level = HttpLoggingInterceptor.Level.NONE;
          break;
      }
      return this;
    }

    Integer getMaxNumberOfRetries() {
      return maxNumberOfRetries;
    }

    Integer getReadTimeout() {
      return readTimeout;
    }

    Integer getConnectionTimeout() {
      return connectionTimeout;
    }

    String getBaseUrl() {
      return baseUrl;
    }

    int getPoolSize() {
      return poolSize;
    }

    long getKeepAliveSeconds() {
      return keepAliveSeconds;
    }

    HttpLoggingInterceptor.Level getLevel() {
      return level;
    }

    public IGameMediaApi build() throws KeyManagementException, NoSuchAlgorithmException {
      return new IGameMediaApiImpl(this);
    }
  }
}
