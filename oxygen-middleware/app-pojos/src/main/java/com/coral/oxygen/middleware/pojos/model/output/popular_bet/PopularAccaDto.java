package com.coral.oxygen.middleware.pojos.model.output.popular_bet;

import java.io.Serializable;
import java.util.List;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class PopularAccaDto implements Serializable {

  private PopularAccaType key;
  private List<String> values;
  private int maxAccas;
  private int minAccas;
  private int thresholdValue;
  private List<String> marketIdentifiers;
}
