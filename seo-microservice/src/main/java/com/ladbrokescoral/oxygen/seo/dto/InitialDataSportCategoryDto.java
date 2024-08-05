package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class InitialDataSportCategoryDto {
  private Integer categoryId;
  private String ssCategoryCode;
  private String targetUri;
  private InitialSportPageConfigDto sportConfig;
}
