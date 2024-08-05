package com.entain.oxygen.betbuilder_middleware.api.response;

import com.entain.oxygen.betbuilder_middleware.api.request.SelectionStatus;
import lombok.Data;

@Data
public class AggPrice {
  String bbHash;
  SelectionStatus suspState;
  Integer statusCode;
  String statusMessage;
  PriceOdds price;
}
