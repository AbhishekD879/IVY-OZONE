package com.ladbrokescoral.oxygen.model;

import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class FreebetTriggerAmount implements Serializable {
  private String currency;
  private String value;
}
