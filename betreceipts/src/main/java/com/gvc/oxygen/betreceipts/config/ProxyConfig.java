package com.gvc.oxygen.betreceipts.config;

import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import org.apache.logging.log4j.util.Strings;
import org.springframework.context.annotation.Configuration;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;
import reactor.netty.transport.ProxyProvider;

@Configuration
public class ProxyConfig {

  private String host = System.getProperty("http.proxyHost");
  private String port = System.getProperty("http.proxyPort");
  private String nonProxyHosts = System.getProperty("http.nonProxyHosts", "localhost");

  /**
   * HttpClient is immutable, and we need two versions of the client i.e., one with proxy set and
   * one without proxy
   *
   * @param connectTimeout
   * @param readTimeout
   * @param writeTimeout
   * @return
   */
  public HttpClient getBppHttpClient(
      String poolName, int poolSize, int connectTimeout, int readTimeout, int writeTimeout) {
    if (isProxyConfigValid())
      return HttpClient.create(ConnectionProvider.create(poolName, poolSize))
          .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeout)
          .option(ChannelOption.SO_KEEPALIVE, true)
          .proxy(
              ops ->
                  ops.type(ProxyProvider.Proxy.HTTP)
                      .host(host)
                      .port(Integer.parseInt(port))
                      .nonProxyHosts(nonProxyHosts))
          .doOnConnected(
              con ->
                  con.addHandlerLast(new ReadTimeoutHandler(readTimeout))
                      .addHandlerLast(new WriteTimeoutHandler(writeTimeout)));
    else
      return HttpClient.create(ConnectionProvider.create(poolName, poolSize))
          .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeout)
          .option(ChannelOption.SO_KEEPALIVE, true)
          .doOnConnected(
              con ->
                  con.addHandlerLast(new ReadTimeoutHandler(readTimeout))
                      .addHandlerLast(new WriteTimeoutHandler(writeTimeout)));
  }

  private boolean isProxyConfigValid() {
    return Strings.isNotEmpty(host) && Strings.isNotEmpty(port);
  }
}
