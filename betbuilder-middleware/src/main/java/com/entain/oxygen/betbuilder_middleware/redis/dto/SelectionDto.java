package com.entain.oxygen.betbuilder_middleware.redis.dto;

import jakarta.validation.constraints.NotNull;
import java.io.Serializable;
import lombok.Data;

@Data
public class SelectionDto implements Serializable {
  private static final long serialVersionUID = 8700132876665387314L;
  String fixtureId;
  @NotNull Long marketId;
  @NotNull Long optionId;
}
