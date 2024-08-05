package com.entain.oxygen.betbuilder_middleware.bpg.model;

import java.util.List;
import lombok.Data;

@Data
public class BPGPriceResponse {
  private String batchError;
  private String batchId;
  private List<Price> prices;
}
