package com.ladbrokescoral.oxygen.model;

import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class LimitEntry implements Serializable {
  private int limitId;
  private String limitSort;
  private String limitRemaining;
  private LimitDefinition limitDefinition;
}
