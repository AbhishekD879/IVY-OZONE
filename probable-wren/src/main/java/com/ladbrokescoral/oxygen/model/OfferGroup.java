package com.ladbrokescoral.oxygen.model;

import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class OfferGroup implements Serializable {
  private String offerGroupId;

  private String offerGroupName;
}
