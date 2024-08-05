package com.oxygen.publisher.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@Data
@NoArgsConstructor
public class VirtualSportEvents {

  private String sportName;
  private int liveEventCount;
}
