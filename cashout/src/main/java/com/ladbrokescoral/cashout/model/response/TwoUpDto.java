package com.ladbrokescoral.cashout.model.response;

import java.util.List;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class TwoUpDto {

  private String selectionId;
  private List<String> betIds;
  private boolean isTwoUpSettled;
}
