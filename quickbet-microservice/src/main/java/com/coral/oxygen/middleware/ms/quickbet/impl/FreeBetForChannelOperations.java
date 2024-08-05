package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.bpp.api.model.bet.api.response.AccFreebetsResponseModel;
import com.coral.bpp.api.model.bet.api.response.AccountFreebetsResponse;
import com.coral.bpp.api.model.bet.api.response.FreebetToken;
import com.coral.bpp.api.model.bet.api.response.GeneralResponse;
import com.coral.bpp.api.service.BppService;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class FreeBetForChannelOperations {

  private final BppService bppService;

  public void restoreState(Session session) {
    if (session.getBanachSelectionData() != null) {
      requestFreeBetTokensForChannel(session, session.getFreeBetForChannelRequestData());
    }
  }

  void requestFreeBetTokensForChannel(Session session, FreeBetForChannelRequestData requestData) {
    session.setFreeBetForChannelRequestData(requestData);
    session.save();

    GeneralResponse<AccountFreebetsResponse> response =
        bppService.accountFreebets(requestData.getToken(), null);
    if (response.getErrorBody() == null) {
      AccountFreebetsResponse body = response.getBody();
      List<FreebetToken> freebetTokens = body.getResponse().getModel().getFreebetToken();
      if (StringUtils.isNoneEmpty(requestData.getChannel())) {
        AccFreebetsResponseModel responseModel = body.getResponse().getModel();
        freebetTokens =
            responseModel.getFreebetToken().stream()
                .filter(t -> t.getTokenPossibleBet() != null)
                .filter(
                    t -> t.getTokenPossibleBet().getChannels().contains(requestData.getChannel()))
                .collect(Collectors.toList());
      }
      session.sendData(Messages.FREE_BET_FOR_CHANNEL_SUCCESS.code(), freebetTokens);
    } else {
      clearRequest(session);
      session.sendData(Messages.FREE_BET_FOR_CHANNEL_ERROR.code(), response.getErrorBody());
    }
  }

  private void clearRequest(Session session) {
    session.setFreeBetForChannelRequestData(null);
    session.save();
    session.unsubscribeFromAllRooms();
  }
}
