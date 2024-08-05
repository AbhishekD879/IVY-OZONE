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
@ConfigurationProperties(prefix = "reactions")
@Data
public class ReactionPropertiesConfig {

  private String cmsBaseUrl;
  private String cmsSurfaceBetApiPath;
  private String cmsHealthApiPath;
  private Integer batchSize;
  private String bppBaseUrl;
  private String bppTokenApiPath;
}
