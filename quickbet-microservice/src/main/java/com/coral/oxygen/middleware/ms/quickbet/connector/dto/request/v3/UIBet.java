package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3;

import io.vavr.collection.List;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class UIBet {
  private String betNo;
  private String winType;
  private String stakePerLine;
  private String betType;
  private List<UILeg> legs;
  private List<String> freebetTokenIds;
}
