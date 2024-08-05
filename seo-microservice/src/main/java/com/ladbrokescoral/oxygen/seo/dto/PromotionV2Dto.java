package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PromotionV2Dto {

  @JsonProperty("title")
  private String title;

  @JsonProperty("promoKey")
  private String promoKey;

  @JsonProperty("shortDescription")
  private String shortDescription;

  @JsonProperty("description")
  private String description;

  @JsonProperty("filename")
  private String filename;
}
