package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

/**
 * Represents the Price model. Copied from Middleware Service.
 *
 * @author tvuyiv
 */
@Data
@JsonInclude(JsonInclude.Include.ALWAYS)
public class OutputPrice implements IdentityAggregator {

  private String id;
  private String priceType;
  private Integer priceNum;
  private Integer priceDen;
  private Double priceDec;
  private String handicapValueDec;
  private Double rawHandicapValue;
  private String priceStreamType;
  private Integer priceAmerican;
}
