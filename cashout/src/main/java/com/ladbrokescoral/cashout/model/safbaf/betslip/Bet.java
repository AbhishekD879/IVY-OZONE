package com.ladbrokescoral.cashout.model.safbaf.betslip;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class Bet {
  private String betKey;
  private String betId;
  private String betType;
  private String betTypeName;
  private String stake;
  private String legType;
  private List<Leg> leg = new ArrayList<>();
  private Double cashoutAmount;
  private String cashoutStatus;
  private String cumulativeStrikePrice;
  private String cumulativeStrikeTrueChance;
  private String driftBoundary;
  private String premium;
  private String cashoutDelayKey;
  private String cashoutDelay;
  private Double freebetAmount;
  private String betPlacedTime;
  private String channelCode;
  private String betReciept;
  private String betStatus;
  private String createDateTime;
  private Double maxStake;
  private Double minStake;
  private Double winningAmount;
  private Double refundAmount;
  private Double bonusAmount;
  private Double stakePerLine;
  private Double fundedAmount;
  private String currencyCode;
  private Double potentialPayout;
  private Integer numberOfLegs;
  private Integer numberOfSelections;
  private Integer numberOfLines;
  private Integer numberOfLinesVoided;
  private Integer numberOfLinesWon;
  private Integer numberOfLinesLost;
  private String settleMethod;
  private String settlementDateTime;
  private String groupId;
  private Integer groupOrder;
  private String groupType;
  private List<SelectionGroup> selectionGroup = new ArrayList<>();
  private List<Integer> selectionKey = new ArrayList<>();
  private List<EligibleBetType> eligibleBetType = new ArrayList<>();
  private List<Promotion> promotions = new ArrayList<>();
  private Integer subjectToBetKey;
  private Double subjectToStake;
  private Double totalStake;
  private List<EnhancedPriceList> enhancedPriceList = new ArrayList<>();
  private String betMessage;
  private String action;
  private Boolean pending;
  private Boolean settled;
}