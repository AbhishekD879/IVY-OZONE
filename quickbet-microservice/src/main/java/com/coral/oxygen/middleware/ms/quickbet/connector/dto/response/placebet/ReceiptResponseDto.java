package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet;

import com.entain.oxygen.bettingapi.model.bet.api.response.accountHistory.response.BetTags;
import com.entain.oxygen.bettingapi.model.bet.api.response.oxi.base.ClaimedOffer;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@NoArgsConstructor
@Accessors(chain = true)
public class ReceiptResponseDto {
  private PriceDto price;
  private ReceiptDto receipt;
  private String date;
  private StakeDto stake;
  private PayoutDto payout;
  private BetDto bet;
  private List<LegPartDto> legParts;
  private Boolean oddsBoost;
  private List<ClaimedOffer> claimedOffers;
  private Long freebetId;
  private BetTags betTags;
}
