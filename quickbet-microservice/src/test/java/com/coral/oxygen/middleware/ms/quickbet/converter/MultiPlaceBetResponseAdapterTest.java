package com.coral.oxygen.middleware.ms.quickbet.converter;

import static org.assertj.core.api.Assertions.assertThat;

import com.entain.oxygen.bettingapi.model.bet.api.common.placeBetV2.BetId;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.BetPlacement;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespStatus;
import io.vavr.collection.List;
import org.junit.jupiter.api.Test;

class MultiPlaceBetResponseAdapterTest {

  @Test
  void shouldReturnThatIsOveraskWhenAnyOfTheBetsHasStatusPending() {
    // GIVEN
    BetPlacement betPlacement1 = createRespBetPlace(RespStatus.A);
    BetPlacement betPlacement2 = createRespBetPlace(RespStatus.P);

    RespBetPlace respBetPlace = new RespBetPlace();
    respBetPlace.getBetPlacement().add(betPlacement1);
    respBetPlace.getBetPlacement().add(betPlacement2);

    MultiPlaceBetResponseAdapter adapter = new MultiPlaceBetResponseAdapter(respBetPlace);

    // WHEN
    boolean isOverask = adapter.isOverask();
    // THEN
    assertThat(isOverask).isTrue();

    List<Long> ids = adapter.getIds();

    assertThat(ids).hasSize(1);
  }

  BetPlacement createRespBetPlace(RespStatus respStatus) {
    Bet bet = new Bet();
    BetId betId = new BetId();
    betId.setContent("911440");
    bet.setBetId(betId);
    bet.setStatus(respStatus);

    BetPlacement betPlacement = new BetPlacement();
    betPlacement.setBet(bet);
    return betPlacement;
  }
}
