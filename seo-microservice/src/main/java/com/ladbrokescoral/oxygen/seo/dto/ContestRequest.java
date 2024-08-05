package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class ContestRequest {
  private String brand;
  private String eventId;
  private String contestId;
  private String userId;
  private String token;
}
