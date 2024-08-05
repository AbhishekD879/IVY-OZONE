package com.entain.oxygen.betbuilder_middleware.bpg.model;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class Selection {

  @NotNull private String fixtureId;
  @NotNull private Long marketId;
  @NotNull private Long optionId;
}
