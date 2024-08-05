package com.gvc.oxygen.betreceipts.entity;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class NextRacesResult {

  private boolean isNextRace;

  private List<NextRace> races = new ArrayList<>();
}
