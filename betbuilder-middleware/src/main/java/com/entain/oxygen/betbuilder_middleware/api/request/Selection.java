package com.entain.oxygen.betbuilder_middleware.api.request;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class Selection {

  private String fixtureId;
  @NotNull private Long marketId;
  @NotNull private Long optionId;
}
