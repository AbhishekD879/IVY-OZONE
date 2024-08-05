package com.ladbrokescoral.oxygen.trendingbets.dto;

import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import java.util.List;
import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class PopularAccaResponse {

  private List<TrendingPosition> positions;
}
