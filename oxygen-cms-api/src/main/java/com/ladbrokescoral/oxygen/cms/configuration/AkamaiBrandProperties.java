package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.exception.AkamaiConfigurationException;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import javax.annotation.PostConstruct;
import lombok.Data;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Slf4j
@Component
@EnableConfigurationProperties
@ConfigurationProperties(prefix = "akamai.brand")
public class AkamaiBrandProperties {

  private Map<String, AkamaiBrandConfig> configs = new HashMap<>();

  @PostConstruct
  private void validateConfigs() {
    log.info("Akamai brand configuration initialized: {}", configs);
    configs.forEach(
        (brand, config) -> {
          if (!config.isEnabled()) {
            log.debug("{} brand Akamai config is disabled", brand);
            return;
          }

          if (StringUtils.isBlank(config.getStoreType())) {
            config.setStoreType(AkamaiStoreType.FILE.getValue());
          }
          if (AkamaiStoreType.OBJECT.getValue().equalsIgnoreCase(config.getStoreType())
              && StringUtils.isBlank(config.getUploadCpcode())) {
            log.error("Akamai upload Cpcode wasn't provided for {} brand ObjectStore", brand);
            throw new AkamaiConfigurationException("Akamai Cpcode not provided");
          }
          if (StringUtils.isBlank(config.getBasePath())) {
            log.error("Akamai basePath wasn't provided for {} brand", brand);
            throw new AkamaiConfigurationException("Akamai basepath not provided");
          }
          if (Objects.isNull(config.getUrl()) || config.getUrl().length == 0) {
            log.error("Akamai url wasn't provided for {} brand", brand);
            throw new AkamaiConfigurationException("Akamai URL not provided");
          }
        });
  }

  @Data
  public static class AkamaiBrandConfig {
    private boolean enabled;
    private String storeType;
    private String uploadCpcode;
    private String host;
    private String key;
    private String keyName;
    private String basePath;
    private String[] url;
  }

  @Getter
  @RequiredArgsConstructor
  private enum AkamaiStoreType {
    FILE("FileStore"),
    OBJECT("ObjectStore");

    private final String value;
  }
}
