package com.ladbrokescoral.oxygen.notification.configs;

/*
   proxy configuration class for the Apns Client
*/

import com.turo.pushy.apns.ApnsClientBuilder;
import com.turo.pushy.apns.proxy.HttpProxyHandlerFactory;
import java.net.InetSocketAddress;
import lombok.extern.slf4j.Slf4j;
import org.apache.logging.log4j.util.Strings;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class ProxyConfig {

  private String host = System.getProperty("http.proxyHost");

  private String port = System.getProperty("http.proxyPort");

  public ApnsClientBuilder proxy(ApnsClientBuilder apnsClientBuilder) {
    if (isProxyConfigValid()) {
      logger.info("Apns client going through the proxy with host: {} and port: {}", host, port);
      return apnsClientBuilder.setProxyHandlerFactory(
          new HttpProxyHandlerFactory(new InetSocketAddress(host, Integer.parseInt(port))));
    }
    return apnsClientBuilder;
  }

  private boolean isProxyConfigValid() {
    return Strings.isNotEmpty(host) && Strings.isNotEmpty(port);
  }
}
