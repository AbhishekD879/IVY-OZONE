package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputMarket;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.entain.oxygen.bettingapi.model.bet.api.common.DocRef;
import com.entain.oxygen.bettingapi.model.bet.api.common.IdRef;
import com.entain.oxygen.bettingapi.model.bet.api.common.LegPart;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.BuildBetsDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.Leg;
import com.entain.oxygen.bettingapi.model.bet.api.request.LegGroup;
import com.entain.oxygen.bettingapi.model.bet.api.request.Price;
import com.entain.oxygen.bettingapi.model.bet.api.request.SportsLeg;
import com.entain.oxygen.bettingapi.model.bet.api.response.OutcomeRef;
import java.util.Arrays;
import java.util.Collections;
import java.util.function.Function;
import org.springframework.stereotype.Component;

@Component
public class RegularSelectionResponseToBuildBetDtoConverter
    extends BaseConverter<RegularSelectionResponse, BuildBetsDto> {

  @Override
  protected BuildBetsDto createTarget() {
    return new BuildBetsDto();
  }

  @Override
  protected BuildBetsDto populateResult(
      RegularSelectionResponse response, BuildBetsDto buildBetsDto) {
    OutputMarket outputMarket = response.getEvent().getMarkets().get(0);
    if (Boolean.TRUE.equals(outputMarket.getIsEachWayAvailable())) {
      buildBetsDto.setLeg(
          Arrays.asList(
              buildLeg("1", "WIN").apply(response), buildLeg("2", "EACH_WAY").apply(response)));
    } else {
      buildBetsDto.setLeg(Collections.singletonList(buildLeg("1", "WIN").apply(response)));
    }
    LegGroup legGroup = new LegGroup();
    DocRef docRef = new DocRef();
    docRef.setDocumentId("1");
    legGroup.setLegRef(Collections.singletonList(docRef));
    buildBetsDto.setLegGroup(Collections.singletonList(legGroup));
    buildBetsDto.setChannelRef(new IdRef("M"));
    buildBetsDto.setReturnOffers(YesNo.N);
    return buildBetsDto;
  }

  private LegPart getLegPart(OutputMarket outputMarket) {
    LegPart legPart = new LegPart();
    legPart.setOutcomeRef(new OutcomeRef(outputMarket.getOutcomes().get(0).getId()));
    return legPart;
  }

  private Price buildBetPrice(OutputPrice selectionPrice) {
    if (selectionPrice != null) {
      Price price = new Price();
      price.setDen(selectionPrice.getPriceDen());
      price.setNum(selectionPrice.getPriceNum());
      price.setPriceTypeRef(new IdRef(selectionPrice.getPriceType()));
      return price;
    } else {
      Price price = new Price();
      price.setPriceTypeRef(new IdRef("SP"));
      return price;
    }
  }

  private Function<RegularSelectionResponse, Leg> buildLeg(String documentId, String winPlaceRef) {
    return response ->
        Leg.builder()
            .documentId(documentId)
            .sportsLeg(
                SportsLeg.builder()
                    .price(buildBetPrice(response.getSelectionPrice()))
                    .winPlaceRef(new IdRef(winPlaceRef))
                    .legPart(getLegPart(response.getEvent().getMarkets().get(0)))
                    .build())
            .build();
  }
}
