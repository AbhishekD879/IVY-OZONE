package com.ladbrokescoral.oxygen.model;

import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class LimitParam implements Serializable {
  private String name;
  private int value;
}
