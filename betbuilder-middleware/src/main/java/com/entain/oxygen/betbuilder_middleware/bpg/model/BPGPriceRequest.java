package com.entain.oxygen.betbuilder_middleware.bpg.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class BPGPriceRequest {
  private String batchId;
  private List<Combination> combinations;

  public List<Combination> getCombinations() {
    if (combinations == null) {
      combinations = new ArrayList<>();
    }
    return combinations;
  }
}
