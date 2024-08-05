package com.entain.oxygen.betbuilder_middleware.bpg.model;

import lombok.Data;

@Data
public class LegInformation {
  private String legId;
  private String clid;
  private Integer suspensionState;
  private Integer resultState;
}
