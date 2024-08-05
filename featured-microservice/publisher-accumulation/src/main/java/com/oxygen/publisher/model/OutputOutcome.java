package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;

/**
 * Represents the Outcome model. Copied from Middleware Service.
 *
 * @author tvuyiv
 */
@Data
@JsonInclude(JsonInclude.Include.ALWAYS)
public class OutputOutcome implements IdentityAggregator {

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
  private String bwinId;
}
