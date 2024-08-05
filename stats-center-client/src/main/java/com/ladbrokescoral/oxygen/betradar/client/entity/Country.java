package com.ladbrokescoral.oxygen.betradar.client.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Country {
  private String id; // 177
  private String name; // Russia
  private String iso; // RUS
}
