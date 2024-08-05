package com.ladbrokescoral.oxygen.notification.entities.bet;

import com.google.gson.annotations.SerializedName;
import java.util.List;
import lombok.Data;

@Data
public class Bet {
  private String betKey;
  private String betId;
  private String betType;
  private String betTypeName;
  private double stake;
  private String legType;

  @SerializedName("leg")
  private List<Leg> legs;

  private double cashoutAmount;
  private String cashoutStatus;
  private String cumulativeStrikePrice;
  private String cumulativeStrikeTrueChance;
  private String driftBoundary;
  private String premium;
  private String cashoutDelayKey;
  private String cashoutDelay;
  private double freebetAmount;
  private String betPlacedTime;
  private String channelCode;
  private String betReceipt;
  private String betStatus;
  private String createDateTime;
  private double maxStake;
  private double minStake;
  private double winningAmount;
  private double refundAmount;
  private double bonusAmount;
  private double stakePerLine;
  private double fundedAmount;
  private String currencyCode;
  private double potentialPayout;
  private int numberOfLegs;
  private int numberOfSelections;
  private int numberOfLines;
  private int numberOfLinesVoided;
  private int numberOfLinesWon;
  private int numberOfLinesLost;
  private String settleMethod;
  private String settlementDateTime;
  private String groupId;
  private int groupOrder;
  private String groupType;
  private List selectionGroup;
  private List selectionKey;
  private List eligibleBetType;
  private List promotions;
  private int subjectToBetKey;
  private double subjectToStake;
  private double totalStake;
  private List enhancedPriceList;
  private String betMessage;
  private String action;
  private Boolean pending;
  private Boolean settled;
}
