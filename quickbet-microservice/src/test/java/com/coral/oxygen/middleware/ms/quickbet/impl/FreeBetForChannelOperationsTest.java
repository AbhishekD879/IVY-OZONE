package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.response.AccountFreebetsResponse;
import com.coral.bpp.api.model.bet.api.response.ErrorBody;
import com.coral.bpp.api.model.bet.api.response.FreebetToken;
import com.coral.bpp.api.model.bet.api.response.GeneralResponse;
import com.coral.bpp.api.service.BppService;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class FreeBetForChannelOperationsTest {

  @Mock private BppService bppServiceMock;
  @Mock private Session sessionMock;

  private FreeBetForChannelOperations operations;

  @BeforeEach
  void setUp() {
    operations = new FreeBetForChannelOperations(bppServiceMock);
  }

  @Test
  void testRequestSuccess() {

    FreeBetForChannelRequestData requestData =
        TestUtils.deserializeWithGson(
            "impl/freeBetForChannelOperations/request.json", FreeBetForChannelRequestData.class);
    AccountFreebetsResponse responseDataBPP =
        TestUtils.deserializeWithGson(
            "impl/freeBetForChannelOperations/responseBPP_success.json",
            AccountFreebetsResponse.class);
    GeneralResponse<AccountFreebetsResponse> generalResponse =
        new GeneralResponse<>(responseDataBPP, null);
    when(bppServiceMock.accountFreebets(requestData.getToken(), null)).thenReturn(generalResponse);

    List<FreebetToken> responseData =
        TestUtils.deserializeListWithJackson(
            "impl/freeBetForChannelOperations/response_success.json", FreebetToken.class);

    operations.requestFreeBetTokensForChannel(sessionMock, requestData);

    verify(sessionMock).sendData(Messages.FREE_BET_FOR_CHANNEL_SUCCESS.code(), responseData);
  }

  @Test
  void testRequestUnauthorized() {
    FreeBetForChannelRequestData requestData =
        TestUtils.deserializeWithGson(
            "impl/freeBetForChannelOperations/request_unauthorized.json",
            FreeBetForChannelRequestData.class);
    ErrorBody responseData =
        TestUtils.deserializeWithGson(
            "impl/freeBetForChannelOperations/response_unauthorized.json", ErrorBody.class);
    GeneralResponse<AccountFreebetsResponse> generalResponse =
        new GeneralResponse<>(null, responseData);
    when(bppServiceMock.accountFreebets(requestData.getToken(), null)).thenReturn(generalResponse);

    operations.requestFreeBetTokensForChannel(sessionMock, requestData);

    verify(sessionMock).sendData(Messages.FREE_BET_FOR_CHANNEL_ERROR.code(), responseData);
  }

  @Test
  void testRestoreState() {
    // given
    FreeBetForChannelRequestData requestData =
        TestUtils.deserializeWithGson(
            "impl/freeBetForChannelOperations/request.json", FreeBetForChannelRequestData.class);
    AccountFreebetsResponse responseDataBPP =
        TestUtils.deserializeWithGson(
            "impl/freeBetForChannelOperations/responseBPP_success.json",
            AccountFreebetsResponse.class);
    GeneralResponse<AccountFreebetsResponse> generalResponse =
        new GeneralResponse<>(responseDataBPP, null);
    when(bppServiceMock.accountFreebets(requestData.getToken(), null)).thenReturn(generalResponse);

    List<FreebetToken> responseData =
        TestUtils.deserializeListWithJackson(
            "impl/freeBetForChannelOperations/response_success.json", FreebetToken.class);

    when(sessionMock.getBanachSelectionData()).thenReturn(new BanachSelectionRequestData());
    when(sessionMock.getFreeBetForChannelRequestData()).thenReturn(requestData);

    // when
    operations.restoreState(sessionMock);

    // then
    verify(sessionMock).sendData(Messages.FREE_BET_FOR_CHANNEL_SUCCESS.code(), responseData);
  }
}
