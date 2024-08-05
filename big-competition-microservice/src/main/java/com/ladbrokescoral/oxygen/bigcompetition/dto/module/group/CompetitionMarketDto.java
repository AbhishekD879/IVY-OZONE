package com.ladbrokescoral.oxygen.bigcompetition.dto.module.group;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.bigcompetition.dto.AbstractEntity;
import com.ladbrokescoral.oxygen.bigcompetition.dto.ViewType;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionMarketDto extends AbstractEntity {
  private String marketId;
  private String nameOverride;
  private int maxDisplay;
  private ViewType viewType;
  private boolean collapsed;
  private EventDto data;
}
