package com.entain.oxygen.betbuilder_middleware.redis.dto;

import java.io.Serializable;
import lombok.Data;

@Data
public class OddsDto implements Serializable {
  private static final long serialVersionUID = 8700132876665387314L;
  Integer american;
  Double decimal;
  FractionalDto fractional;
}
