package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

/** Created by JacksonGenerator on 11/23/17. */
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class BirResponse {
  @JsonProperty("confirmationExpectedAt")
  private String confirmationExpectedAt;

  @JsonProperty("provider")
  private String provider;
}
