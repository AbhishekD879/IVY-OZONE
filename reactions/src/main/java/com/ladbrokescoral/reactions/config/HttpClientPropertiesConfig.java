package com.ladbrokescoral.reactions.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * @author PBalarangakumar 15-06-2023
 */
@Configuration
@EnableConfigurationProperties
@ConfigurationProperties(prefix = "reactions.http.client")
@Data
public class HttpClientPropertiesConfig {

  private int connectTimeout;

  private boolean keepAlive;

  private int readTimeout;

  private int responseTimeout;
}
