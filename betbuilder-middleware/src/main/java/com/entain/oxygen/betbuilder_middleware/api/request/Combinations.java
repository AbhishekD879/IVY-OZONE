package com.entain.oxygen.betbuilder_middleware.api.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class Combinations {
  @NotBlank(message = "Please input valid bbHash")
  String bbHash;
}
