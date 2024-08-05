package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import lombok.Data;

@Data
public class TierInfo {
  private String tierName;
  private List<String> offerIdSeq;
  private List<Integer> freeBetPositionSequence;
}
