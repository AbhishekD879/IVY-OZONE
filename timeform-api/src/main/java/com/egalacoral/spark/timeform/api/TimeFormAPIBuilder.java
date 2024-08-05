package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.connectivity.FailOverStrategy;
import com.egalacoral.spark.timeform.api.connectivity.NoFailOverStrategy;
import com.egalacoral.spark.timeform.api.connectivity.SystemTimeProvider;
import com.egalacoral.spark.timeform.api.connectivity.TimeProvider;

/**
 * Builder for creation and configuration TimeFormAPI instance
 * */
public class TimeFormAPIBuilder {

  private final String loginUrl;

  private final String dataUrl;

  private TimeProvider timeProvider = new SystemTimeProvider();

  private FailOverStrategy failOverStrategy = new NoFailOverStrategy();

  /**
   * @param loginUrl  base Url for login service (e.g. 'https://sso.timeform.com')
   * @param dataUrl   base Url for data receiving service (e.g. 'https://sso.timeform.com')
   * */
  public TimeFormAPIBuilder(String loginUrl, String dataUrl) {
    this.loginUrl = loginUrl;
    this.dataUrl = dataUrl;
  }

  /**
   * Creates configured instance of TimeFormAPI
   *
   * @return configured instance of TimeFormAPI
   * */
  public TimeFormAPI build() {
    return new TimeFormAPI(loginUrl, dataUrl, timeProvider, failOverStrategy);
  }

  /**
   * Configure TimeFormAPI to use custom TimeProvider
   *
   * By default SystemTimeProvider is used.
   * */
  public TimeFormAPIBuilder setTimeProvider(TimeProvider timeProvider) {
    this.timeProvider = timeProvider;
    return this;
  }

  /**
   * Configure TimeFormAPI to use custom FailOverStrategy
   *
   * By default NoFailOverStrategy is used without any failover functionality.
   * You can use also RetryReloginFailOverStrategy implemented in library
   * */
  public TimeFormAPIBuilder setFailOverStrategy(FailOverStrategy failOverStrategy) {
    this.failOverStrategy = failOverStrategy;
    return this;
  }
}
