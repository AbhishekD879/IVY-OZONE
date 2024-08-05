package com.coral.oxygen.middleware.pojos.model.output.popular_bet;

import java.io.Serializable;
import java.util.List;
import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class PopularAccaResponse implements Serializable {

  private List<TrendingPosition> positions;
}
