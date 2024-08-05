package com.ladbrokescoral.cashout.util;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.Code;
import com.ladbrokescoral.cashout.model.SSEType;
import com.ladbrokescoral.cashout.model.response.*;
import java.util.List;
import java.util.Objects;
import lombok.experimental.UtilityClass;
import org.springframework.http.codec.ServerSentEvent;

@UtilityClass
public class SSEFactory {

  public static ServerSentEvent<BetResponse> update(UpdateDto data) {
    if (Objects.nonNull(data.getBet())) {
      return ServerSentEvent.<BetResponse>builder()
          .event(SSEType.BET_UPDATE.getValue())
          .data(new UpdateBetResponse(data.getBet()))
          .build();
    } else {
      return ServerSentEvent.<BetResponse>builder()
          .event(SSEType.CASHOUT_UPDATE.getValue())
          .data(new UpdateCashoutResponse(data.getCashoutData(), data.getError()))
          .build();
    }
  }

  public static ServerSentEvent<BetResponse> initial(List<Bet> data) {
    return ServerSentEvent.<BetResponse>builder()
        .event(SSEType.INITIAL.getValue())
        .data(new InitialBetResponse(data))
        .build();
  }

  public static ServerSentEvent<BetResponse> initialAccHistory(List<BetSummaryModel> data) {
    return ServerSentEvent.<BetResponse>builder()
        .event(SSEType.INITIAL.getValue())
        .data(new InitialAccountHistoryBetResponseModel(data))
        .build();
  }

  public static ServerSentEvent<BetResponse> error(Code data, SSEType sseType) {
    return ServerSentEvent.<BetResponse>builder()
        .event(sseType.getValue())
        .data(ErrorBetResponse.create(data))
        .build();
  }
}
