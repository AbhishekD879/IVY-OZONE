package com.entain.oxygen.dto;

import lombok.Data;

@Data
public class ChildrenDto {
  private EventDto event;
  private MarketDto market;
  private OutcomeDto outcome;
  private PriceDto price;
}
