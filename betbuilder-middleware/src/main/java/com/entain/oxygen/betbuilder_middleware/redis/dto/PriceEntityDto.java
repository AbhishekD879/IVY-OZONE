package com.entain.oxygen.betbuilder_middleware.redis.dto;

import java.io.Serializable;
import lombok.Data;
import lombok.ToString;

@Data
@ToString
public class PriceEntityDto implements Serializable {
  private static final long serialVersionUID = 8700132876665387314L;
  OddsDto odds;
  Integer status;
}
