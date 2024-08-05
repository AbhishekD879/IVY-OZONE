package com.entain.oxygen.betbuilder_middleware.api.request;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class CheckPriceRequest {

  String transId;

  @Valid
  @NotEmpty(message = "Atleast one combination is mandatory")
  List<Combinations> combinations;

  public List<Combinations> getCombinations() {

    if (combinations == null) {
      combinations = new ArrayList<>();
    }
    return combinations;
  }
}
