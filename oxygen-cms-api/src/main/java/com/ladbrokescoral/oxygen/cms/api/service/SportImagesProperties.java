package com.ladbrokescoral.oxygen.cms.api.service;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/** @author volodymyr.masliy on 27/03/2018 */
@Component
@ConfigurationProperties(value = "images.sports", ignoreInvalidFields = true)
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SportImagesProperties {
  private String path;
  private SizedImage small;
  private SizedImage medium;
  private SizedImage large;
  private IconImageProperties icons;

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  @Builder
  public static class IconImageProperties {
    private SizedImage small;
    private SizedImage medium;
    private SizedImage large;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  @Builder
  public static class SizedImage {
    private String path;
    private String size;
  }
}
