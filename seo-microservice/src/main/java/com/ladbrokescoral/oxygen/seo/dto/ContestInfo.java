package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class ContestInfo {
  private String id;
  private String name;
}
