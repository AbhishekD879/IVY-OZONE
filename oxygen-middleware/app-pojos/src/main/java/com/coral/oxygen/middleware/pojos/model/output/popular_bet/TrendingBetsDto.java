package com.coral.oxygen.middleware.pojos.model.output.popular_bet;

import java.io.Serializable;
import java.util.Set;
import lombok.Data;

@Data
public class TrendingBetsDto implements Serializable {

  private String updatedAt;

  private String lastMsgUpdatedAt;

  private Set<TrendingPosition> positions;
}
