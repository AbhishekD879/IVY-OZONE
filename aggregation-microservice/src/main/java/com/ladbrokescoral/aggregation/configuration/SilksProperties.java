package com.ladbrokescoral.aggregation.configuration;

import com.ladbrokescoral.aggregation.utils.ImageUtils;
import java.awt.image.BufferedImage;
import java.text.MessageFormat;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Objects;
import java.util.Optional;
import javax.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "silks")
@Data
public class SilksProperties {

  private int expectedWidth;
  private int expectedHeight;
  private String expectedExtension;
  private Map<String, Map<String, String>> providers;
  private transient Map<String, ImageProvider> providersWithParsedSilks;

  @PostConstruct
  public void init() {
    providersWithParsedSilks = new HashMap<>();
    for (Entry<String, Map<String, String>> provider : providers.entrySet()) {
      providersWithParsedSilks.put(provider.getKey(), toImageProvider(provider.getValue()));
    }
  }

  private ImageProvider toImageProvider(Map<String, String> imageProviderConfig) {
    Objects.requireNonNull(imageProviderConfig);
    String endpoint = imageProviderConfig.get("endpoint");
    String defaultSilk = imageProviderConfig.get("defaultSilk");
    Objects.requireNonNull(endpoint);
    Objects.requireNonNull(defaultSilk);

    return new ImageProvider(
        endpoint,
        ImageUtils.loadImage(
            this.getClass(), MessageFormat.format("defaultSilks/{0}", defaultSilk)));
  }

  public Optional<ImageProvider> getImageProvider(String provider) {
    return Optional.ofNullable(providersWithParsedSilks.get(provider));
  }

  @Data
  @AllArgsConstructor
  @NoArgsConstructor
  public static class ImageProvider {

    private String endpoint;
    private BufferedImage defaultSilk;
  }
}
