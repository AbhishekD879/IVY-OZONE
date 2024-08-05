package com.entain.oxygen.betbuilder_middleware.api.response;

import java.util.List;
import lombok.Data;

@Data
public class CheckPriceResponse {
  String transId;
  List<AggPrice> prices;
}
