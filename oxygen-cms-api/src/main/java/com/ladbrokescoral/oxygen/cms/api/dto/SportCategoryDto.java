package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class SportCategoryDto extends SportCategoryNativeDto {
  private String svg;
  private String svgId;
  private InitialSportPageConfigDto sportConfig;
}
