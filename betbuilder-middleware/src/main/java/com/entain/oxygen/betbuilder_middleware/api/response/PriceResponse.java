package com.entain.oxygen.betbuilder_middleware.api.response;

import java.util.List;
import lombok.Data;

@Data
public class PriceResponse {
  private String batchError;
  private String batchId;
  private List<Price> prices;
}
