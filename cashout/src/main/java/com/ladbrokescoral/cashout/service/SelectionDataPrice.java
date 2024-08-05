package com.ladbrokescoral.cashout.service;

import lombok.Data;

@Data
public class SelectionDataPrice {
  private final int num;
  private final int den;

  public boolean isCompetitive() {
    return den < num * 100;
  }
}
