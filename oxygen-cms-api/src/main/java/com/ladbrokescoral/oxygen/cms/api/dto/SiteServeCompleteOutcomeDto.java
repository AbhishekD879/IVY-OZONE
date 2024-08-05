package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class SiteServeCompleteOutcomeDto {
  private String id;
  private String name;
  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private String outcomeMeaningScores;
  private Integer runnerNumber;
  private Boolean isResulted;
  private String outcomeStatusCode;
  private String liveServChannels;
  private boolean hasPriceStream;
  private List<PriceDto> prices;
  private Integer displayOrder;
}
