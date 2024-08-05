package com.coral.oxygen.middleware.common.configuration.cfcache;

import static java.util.Objects.requireNonNull;
import static org.apache.commons.lang3.StringUtils.defaultIfBlank;

import java.util.HashMap;
import java.util.Map;
import java.util.stream.Stream;
import javax.annotation.PostConstruct;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Slf4j
@Component
@ConfigurationProperties(prefix = "aws.s3.brand")
public class S3BrandProperties {

  private Map<String, S3BrandConfig> configs = new HashMap<>();

  @PostConstruct
  private void validateConfigs() {
    log.info("S3 brand configuration initialized: {}", configs);
    configs.forEach(
        (String brand, S3BrandConfig config) -> {
          if (config.isEnabled()) {
            requireNonNull(
                defaultIfBlank(config.getBucket(), null), "S3 bucket should not be empty");
            requireNonNull(
                defaultIfBlank(config.getRegion(), null), "S3 region should not be empty");
            requireNonNull(config.getPurgeUrl(), "At least one purgeUrl should be provided");
            requireNonNull(
                Stream.of(config.getPurgeUrl()).findAny().orElse(null),
                "At least one purgeUrl should be provided");
            if (config.isCloudFlarePurgeService()) {
              requireNonNull(
                  defaultIfBlank(config.getPurgeZoneId(), null),
                  "CloudFlare purgeZoneId should not be empty");
            }
          }
        });
  }

  @Data
  public static class S3BrandConfig {
    private boolean enabled;
    private String region;
    private String bucket;
    private String basePath;
    private int reqTimeout;
    // CloudFlare or Akamai
    private String purgeService;
    // For Cloudflare only
    private String purgeZoneId;
    private String[] purgeUrl;

    public boolean isCloudFlarePurgeService() {
      return "CloudFlare".equalsIgnoreCase(purgeService);
    }
  }
}
