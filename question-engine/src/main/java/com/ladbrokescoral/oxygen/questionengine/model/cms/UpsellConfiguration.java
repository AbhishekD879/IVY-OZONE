package com.ladbrokescoral.oxygen.questionengine.model.cms;

import lombok.Data;

import java.util.Map;

@Data
public class UpsellConfiguration {
  private Map<String, Long> options;
  private Long defaultUpsellOption;
  private String fallbackImagePath;
  private String imageUrl;
}
