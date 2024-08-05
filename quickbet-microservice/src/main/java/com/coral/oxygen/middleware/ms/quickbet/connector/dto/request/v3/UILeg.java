package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import io.vavr.collection.List;
import io.vavr.control.Option;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class UILeg {
  private Integer priceNum;
  private Integer priceDen;
  private List<String> outcomeIds;
  private String priceType;
  private Option<ComplexSelection.Type> selectionType;
}
