package com.coral.oxygen.middleware.pojos.model.cms.featured;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class RpgConfig {
  private String title;
  private String seeMoreLink;
  private String bundleUrl;
  private String loaderUrl;
  private Integer gamesAmount;
}
