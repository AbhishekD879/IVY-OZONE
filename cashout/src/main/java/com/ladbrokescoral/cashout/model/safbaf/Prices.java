package com.ladbrokescoral.cashout.model.safbaf;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class Prices {
  private Integer num;
  private List<Price> price = new ArrayList<>();
}
