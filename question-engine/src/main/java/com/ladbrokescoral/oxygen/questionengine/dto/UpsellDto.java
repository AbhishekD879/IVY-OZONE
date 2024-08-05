package com.ladbrokescoral.oxygen.questionengine.dto;

import lombok.Data;
import lombok.experimental.Accessors;

import java.util.Map;

@Data
@Accessors(chain = true)
public class UpsellDto {
  private Map<String, UpsellPriceDto> dynamicUpsellOptions;
  private UpsellPriceDto defaultUpsellOption;
  private String fallbackImagePath;
  private String imageUrl;
}
