package com.ladbrokescoral.oxygen.notification.entities.bet;

import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Meta;
import lombok.Data;

@Data
public class Betslip {
  private String betslipKey;
  private String countryCode;
  private String betChannel;
  private String betslipDateTime;
  private String customerID;
  private String username;
  private String formatType;
  private String formatSize;
  private String takeDateTime;
  private String takenBy;
  private String takeMethod;
  private Boolean captureToFollow;
  private String captureDateTime;
  private String capturedBy;
  private String captureMethod;
  private Boolean isRecapture;
  private String shopNumber;
  private String tillNumber;
  private String barcode;
  private String loyaltyCardNo;
  private Boolean isSettled;
  private String settleMethod;
  private Bets bets;
  private Meta meta;
  private String payoutStatus;
  private String payoutDateTime;
  private String payoutMethod;
  private Boolean isPaidDirect;
  private String settlementStatus;
  private Integer totalBetslipNumOfBets;
  private Double totalBetslipStake;
  private Integer winningBetCount;
  private Boolean valid;
  private Boolean paid;
  private Boolean cancelled;
}
