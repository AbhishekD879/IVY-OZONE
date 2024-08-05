package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import lombok.Data;
import lombok.experimental.Accessors;

import java.util.Map;

@Data
@Accessors(chain = true)
public class UpsellConfigurationDto {
  private Map<String, Long> options;
  private Long defaultUpsellOption;
  private String fallbackImagePath;
  private String imageUrl;
}
