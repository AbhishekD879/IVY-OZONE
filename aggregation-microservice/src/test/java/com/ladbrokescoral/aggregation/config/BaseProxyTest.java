package com.ladbrokescoral.aggregation.config;

import com.ladbrokescoral.aggregation.configuration.ApiProperties;
import com.ladbrokescoral.aggregation.configuration.WebClientConfig;
import java.time.Duration;
import lombok.Getter;
import org.junit.jupiter.api.BeforeEach;

@Getter
public abstract class BaseProxyTest {

  private WebClientConfig webClientConfig;

  private ApiProperties apiProperties;

  protected static final String HOST = "localhost";

  protected static final String PORT = "8888";

  @BeforeEach
  public void init() {
    apiProperties = getApiProperties();
    webClientConfig = new WebClientConfig(apiProperties, 100, 10000);
  }

  private ApiProperties getApiProperties() {
    ApiProperties apiProperties = new ApiProperties();
    ApiProperties.Image image = new ApiProperties.Image();
    image.setConnectionTimeout(Duration.ofSeconds(5));
    image.setWriteTimeout(Duration.ofSeconds(5));
    image.setReadTimeout(Duration.ofSeconds(5));
    image.setNumberOfRetries(3);
    apiProperties.setImage(image);
    return apiProperties;
  }
}
