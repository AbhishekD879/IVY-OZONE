package com.egalacoral.spark.siteserver.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;
import lombok.Data;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
@Data
public class Children {

  private HealthCheck healthCheck;
  private Error error;
  private Coupon coupon;
  private Event event;
  private Market market;
  private Outcome outcome;
  private Price price;
  private Event resultedEvent;
  private Market resultedMarket;
  private Outcome resultedOutcome;
  private Price resultedPrice;
  private ReferenceEachWayTerms referenceEachWayTerms;

  @JsonProperty("class")
  private Category category;

  @JsonProperty("category")
  private CategoryEntity categoryEntity;

  private Type type;
  private Aggregation aggregation;
  private RacingFormOutcome racingFormOutcome;
  private Scorecast scorecast;
  private ResponseFooter responseFooter;
  private MediaProvider mediaProvider;
  private Media media;
  private Map eventPeriod;
  private Map eventParticipant;
  private Pool pool;
  private RacingResult racingResult;
  private FinalPosition finalPosition;
  private NcastDividend ncastDividend;
  private RacingFormEvent racingFormEvent;
  private ExternalKeys externalKeys;
}
