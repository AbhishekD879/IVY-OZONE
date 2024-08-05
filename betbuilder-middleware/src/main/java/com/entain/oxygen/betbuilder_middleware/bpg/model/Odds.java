package com.entain.oxygen.betbuilder_middleware.bpg.model;

import lombok.Data;

@Data
public class Odds {
  private Integer american;
  private Double decimal;
  private Fractional fractional;
}
