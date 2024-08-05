package com.ladbrokescoral.cashout.model.safbaf.betslip;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class SelectionGroup {
  private List<Integer> selectionKey = new ArrayList<>();
  private String groupType;
}
