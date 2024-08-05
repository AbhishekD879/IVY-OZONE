package com.entain.oxygen.betbuilder_middleware.api.response;

import lombok.Data;

@Data
public class Odds {
  private Integer american;
  private Double decimal;
  private Fractional fractional;
}
