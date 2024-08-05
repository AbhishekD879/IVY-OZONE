package com.coral.oxygen.edp.model.output;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class OutputOutcome {
  private String id;
  private String name;
  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private String outcomeMeaningScores;
  private Integer runnerNumber;
  private Boolean isResulted;
  private String outcomeStatusCode;
  private String liveServChannels;
  private String correctPriceType;
  private Boolean icon;
  private Integer correctedOutcomeMeaningMinorCode;
  private Boolean nonRunner;
  private List<OutputPrice> prices;
  private Integer displayOrder;
  private OutputRacingFormOutcome racingFormOutcome;
  private Boolean hasPriceStream;
}
