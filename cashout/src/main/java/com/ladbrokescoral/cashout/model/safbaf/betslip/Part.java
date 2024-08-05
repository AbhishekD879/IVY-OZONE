package com.ladbrokescoral.cashout.model.safbaf.betslip;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class Part {
  private String partNo;
  private String priceType;
  private Price betPrice;

  @JsonProperty("currentPrice")
  private Price currentPrice;

  @JsonProperty("startingPrice")
  private Price startingPrice;

  @JsonProperty("settlementPrice")
  private Price settlementPrice;

  @JsonProperty("placePrice")
  private Price placePrice;

  private String cashoutType;
  private String cashoutLadder;
  private String resultCode;
  private String result;
  private String resultPlaces;
  private String eachWayNum;
  private String eachWayDen;
  private String eachWayPlaces;
  private String placeTerms;
  private String rawHandicapValue;
  private List<DeductionDetail> deductionDetail = new ArrayList<>();
  private BigInteger selectionKey;
  private String selectionName;
  private String outcomeMeaningMinorCode;
  private Integer marketKey;
  private String marketName;
  private String marketSort;
  private Integer eventKey;
  private String eventName;
  private String eventDateTime;
  private Integer typeKey;
  private String typeName;
  private Integer classKey;
  private String className;
  private Integer categoryKey;
  private String categoryName;
  private String runnerNumber;
  private Boolean isResultConfirmed;
  private String resultDateTime;
  private String handicapType;
  private String handicapValue;
  private String marketType;
  private String winPlace;
  private String rawMarketName;
  private String birIndex;
  private String selectionStatus;
  private Boolean isInRunning;
  private Integer accMin;
  private Integer accMax;
  private List<PreviousTerm> previousTerms = new ArrayList<>();
}
