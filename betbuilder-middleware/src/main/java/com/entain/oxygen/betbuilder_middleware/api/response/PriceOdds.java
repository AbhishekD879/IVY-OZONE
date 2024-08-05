package com.entain.oxygen.betbuilder_middleware.api.response;

import lombok.Data;
import lombok.ToString;

@Data
@ToString
public class PriceOdds {
  Double decimal;
  FractionalOdds fractional;
}
