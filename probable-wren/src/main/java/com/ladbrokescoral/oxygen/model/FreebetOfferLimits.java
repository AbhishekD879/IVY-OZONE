package com.ladbrokescoral.oxygen.model;

import java.io.Serializable;
import java.util.List;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class FreebetOfferLimits implements Serializable {
  private List<LimitEntry> limitEntry;
}
