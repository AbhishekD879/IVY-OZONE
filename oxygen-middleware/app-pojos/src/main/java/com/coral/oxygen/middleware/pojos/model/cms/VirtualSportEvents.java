package com.coral.oxygen.middleware.pojos.model.cms;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@Data
@NoArgsConstructor
@EqualsAndHashCode(of = "sportName")
public class VirtualSportEvents {

  private String sportName;
  private int liveEventCount;
}
