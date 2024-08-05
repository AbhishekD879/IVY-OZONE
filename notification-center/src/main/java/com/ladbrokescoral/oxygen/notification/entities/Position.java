package com.ladbrokescoral.oxygen.notification.entities;

import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@Builder
@EqualsAndHashCode
public class Position {
  private String id;
  private Integer position;
  private String name;
  private Integer runnerNumber;
}
