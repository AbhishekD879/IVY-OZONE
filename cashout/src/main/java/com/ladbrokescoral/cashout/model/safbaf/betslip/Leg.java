package com.ladbrokescoral.cashout.model.safbaf.betslip;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class Leg {
  private String legNo;
  private List<Part> part = new ArrayList<>();
  private String legSort;
}
