package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.BetDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.LegPartDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.PayoutDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.PriceDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptResponseDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.StakeDto;
import com.entain.oxygen.bettingapi.model.bet.api.common.LegPart;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.Leg;
import com.entain.oxygen.bettingapi.model.bet.api.response.OutcomeRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.Price;
import com.entain.oxygen.bettingapi.model.bet.api.response.Range;
import com.ladbrokescoral.scoreboards.parser.api.BipParserFactory;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import com.ladbrokescoral.scoreboards.parser.model.EventCategory;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.apache.commons.lang3.math.NumberUtils;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Component
public class BetToReceiptResponseDtoConverter extends BaseConverter<Bet, ReceiptResponseDto> {

  public static final String WIN = "WIN";

  @Override
  public ReceiptResponseDto populateResult(Bet bet, ReceiptResponseDto dto) {

    String freebet = bet.getStake().getFreebet();
    String stakePerLine = bet.getStake().getStakePerLine();
    String amount = bet.getStake().getAmount();
    String freebetOfferCategory = bet.getStake().getFreebetOfferCategory();
    Leg leg = bet.getLeg().get(0);
    List<Price> prices =
        !CollectionUtils.isEmpty(leg.getSportsLeg().getPrices())
            ? leg.getSportsLeg().getPrices()
            : Collections.singletonList(leg.getSportsLeg().getPrice());

    dto.setLegParts(
            leg.getSportsLeg().getLegPart().stream()
                .map(this::convertLegPart)
                .collect(Collectors.toList()))
        .setPrice(getRightPrice(prices))
        .setReceipt(new ReceiptDto().withId(bet.getReceipt()))
        .setStake(
            new StakeDto()
                .withStakePerLine(stakePerLine)
                .withFreebet(freebet)
                .withFreebetOfferCategory(freebetOfferCategory)
                .withAmount(amount))
        .setDate(bet.getTimeStamp())
        .setPayout(new PayoutDto().setPotential(bet.getPayout().get(0).getPotential()))
        .setBet(
            new BetDto()
                .id(bet.getId())
                .isReffered(bet.getIsReferred())
                .isConfirmed(bet.getIsConfirmed())
                .withCashoutValue(bet.getCashoutValue()));
    dto.setOddsBoost(hasOddsBoostToken(bet));
    dto.setClaimedOffers(bet.getClaimedOffers());
    dto.setBetTags(bet.getBetTags());

    return dto;
  }

  private boolean hasOddsBoostToken(Bet bet) {
    return bet.getFreebet() != null
        && !bet.getFreebet().isEmpty()
        && bet.getFreebet().get(0).getType() != null
        && bet.getFreebet().get(0).getType().equals("BETBOOST");
  }

  /*
   * Return always first WIN price. EachWay is used at formula and is not final
   */
  private PriceDto getRightPrice(List<Price> prices) {
    return new PriceDto(
        prices.get(0).getPriceNum(),
        prices.get(0).getPriceDen(),
        prices.get(0).getPriceTypeRef().getId());
  }

  private LegPartDto convertLegPart(LegPart legPart) {
    LegPartDto result = new LegPartDto();
    OutcomeRef outcomeRef = legPart.getOutcomeRef();
    if (outcomeRef != null) {
      result.setOutcomeId(outcomeRef.getId());
      BipComment bipComment =
          EventCategory.from(NumberUtils.toInt(outcomeRef.getEventCategoryId()))
              .map(BipParserFactory::getParser)
              .orElse(BipParserFactory.getUnknownCategoryParser())
              .parse(outcomeRef.getEventDesc());
      if (bipComment.getEventName() != null) {
        result.setEventDesc(bipComment.getEventName().replaceAll("(?i)\\bvs\\b", "v"));
      }
      result.setMarketDesc(outcomeRef.getMarketDesc());
      result.setOutcomeDesc(outcomeRef.getOutcomeDesc());
      result.setEachWayNum(outcomeRef.getEachWayNum());
      result.setEachWayDen(outcomeRef.getEachWayDen());
      result.setEachWayPlaces(outcomeRef.getEachWayPlaces());
      String handicap =
          Optional.ofNullable(legPart.getRange())
              .map(Range::getHigh)
              .map(this::mapHandicap)
              .orElse(null);
      result.setHandicap(handicap);
    }
    return result;
  }

  @Override
  protected ReceiptResponseDto createTarget() {
    return new ReceiptResponseDto();
  }

  private String mapHandicap(String handicap) {
    return !handicap.startsWith("-") ? "+".concat(handicap) : handicap;
  }
}
