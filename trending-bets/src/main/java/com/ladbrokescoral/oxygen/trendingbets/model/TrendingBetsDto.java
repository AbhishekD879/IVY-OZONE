package com.ladbrokescoral.oxygen.trendingbets.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import java.util.Date;
import java.util.Set;
import lombok.Data;
import lombok.experimental.SuperBuilder;

@Data
@SuperBuilder
public class TrendingBetsDto {

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ssX")
  private Date updatedAt;

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ssX")
  private Date lastMsgUpdatedAt;

  private Set<TrendingPosition> positions;
}
