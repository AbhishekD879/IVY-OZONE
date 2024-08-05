package com.ladbrokescoral.oxygen.trendingbets.dto;

import java.io.Serializable;
import java.util.List;
import lombok.Data;

@Data
public class PopularAccaDto implements Serializable {

  private PopularAccaType key;
  private List<String> values;
  private int maxAccas;
  private int minAccas;
  private int thresholdValue;
  private List<String> marketIdentifiers;
}
