package com.entain.oxygen.betbuilder_middleware.api.request;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.ToString;

@Data
@ToString
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class PriceRequest {
  private String batchId;
  private List<Combination> combinations;

  public List<Combination> getCombinations() {
    if (combinations == null) {
      combinations = new ArrayList<>();
    }
    return combinations;
  }
}
