package com.gvc.oxygen.betreceipts.config;

import com.coral.bpp.api.service.BppApiAsync;
import com.coral.bpp.api.service.impl.BppApiAsyncImpl;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import reactor.netty.http.client.HttpClient;

@Configuration
public class BppApiConfigHeavy {

  @Value("${bpp.url}")
  private String url;

  @Value("${bpp.details.retry.number}")
  private int retryNumber;

  @Value("${bpp.details.connect.timeout}")
  private int connectTimeout;

  @Value("${bpp.details.read.timeout}")
  private int readTimeout;

  @Value("${bpp.details.write.timeout}")
  private int writeTimeout;

  @Value("${bpp.details.retry.timeout}")
  private int retryTimeoutMillis;

  @Value("${bpp.details.pool.size:1000}")
  private int poolSize;

  @Value("${bpp.details.pool.timeout:45000}")
  private long poolTimeout;

  private ProxyConfig proxyConfig;

  public BppApiConfigHeavy(ProxyConfig proxyConfig) {
    this.proxyConfig = proxyConfig;
  }

  @Bean
  public BppApiAsync bppApiAsyncHeavy() {
    HttpClient httpClient =
        proxyConfig
            .getBppHttpClient("betDetailsPool", poolSize, connectTimeout, readTimeout, writeTimeout)
            .compress(true);

    return new BppApiAsyncImpl(
        url, retryNumber, retryTimeoutMillis, new ReactorClientHttpConnector(httpClient));
  }
}
