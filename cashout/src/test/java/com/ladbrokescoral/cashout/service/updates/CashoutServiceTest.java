package com.ladbrokescoral.cashout.service.updates;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.google.common.reflect.TypeToken;
import com.ladbrokescoral.cashout.api.client.RemoteCashoutApi;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import com.ladbrokescoral.cashout.converter.BetToCashoutOfferRequestConverter;
import com.ladbrokescoral.cashout.model.response.CashoutData;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.BppService;
import com.ladbrokescoral.cashout.util.GsonUtil;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Function;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class CashoutServiceTest {
  @InjectMocks private CashoutService cashoutOfferService;
  @Mock private BetToCashoutOfferRequestConverter converter;
  @Mock private RemoteCashoutApi remoteCashoutApi;
  @Mock private Function<CashoutOffer, UpdateDto> cashoutOfferToBetUpdate;
  @Mock private BetUpdatesTopic betUpdatesTopic;
  @Mock private BppService bppService;
  @Mock private AsyncCashoutOfferService asyncCashoutOfferService;
  @Mock private AsyncBetDetailService asyncBetDetailService;

  @Test
  void testPrepareCashoutReq() {
    ReflectionTestUtils.setField(cashoutOfferService, "cashoutOfferReqSize", 4);
    BetSummaryModel bet = new BetSummaryModel();
    bet.setId("2345167");
    CashoutOfferRequest cashoutOfferRequest =
        CashoutOfferRequest.builder().cashoutOfferReqRef("2345167").build();
    CashoutRequest cashoutRequest =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(cashoutOfferRequest))
            .shouldActivate(true)
            .build();

    CashoutOffer cashoutOffer =
        CashoutOffer.builder().cashoutOfferReqRef("2341567").cashoutValue(2.30).build();
    CashoutData cashoutData =
        CashoutData.builder().betId("2341678").cashoutStatus("Active").cashoutValue("2.30").build();
    UpdateDto updateDto = UpdateDto.builder().cashoutData(cashoutData).build();
    when(converter.convert(Mockito.any())).thenReturn(cashoutRequest);
    cashoutOfferService.prepareCashoutReq(Collections.singleton(bet), false);
  }

  @Test
  void testPrepareCashoutReq_cashout_Null() {
    ReflectionTestUtils.setField(cashoutOfferService, "cashoutOfferReqSize", 4);
    BetSummaryModel bet = new BetSummaryModel();
    bet.setId("2345167");
    CashoutOfferRequest cashoutOfferRequest =
        CashoutOfferRequest.builder().cashoutOfferReqRef("2345167").build();
    CashoutRequest cashoutRequest =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(cashoutOfferRequest))
            .shouldActivate(true)
            .build();
    CashoutOffer cashoutOffer = CashoutOffer.builder().cashoutValue(2.30).build();
    when(converter.convert(Mockito.any())).thenReturn(cashoutRequest);
    cashoutOfferService.prepareCashoutReq(Collections.singleton(bet), false);
    verify(betUpdatesTopic, times(0)).sendBetUpdate(Mockito.any(), Mockito.any());
  }

  @Test
  void testCashoutReq_size() {
    ReflectionTestUtils.setField(cashoutOfferService, "cashoutOfferReqSize", 1);
    CashoutOfferRequest cashoutOfferRequest =
        CashoutOfferRequest.builder().cashoutOfferReqRef("123").build();
    CashoutRequest cashoutReq =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(cashoutOfferRequest))
            .shouldActivate(true)
            .build();
    CashoutOffer cashoutOffer = CashoutOffer.builder().cashoutValue(2.30).build();
    when(converter.convert(Mockito.any())).thenReturn(cashoutReq);
    cashoutOfferService.prepareCashoutReq(getBets("BetSummaryModel8.json"), false);
    verify(betUpdatesTopic, times(0)).sendBetUpdate(Mockito.any(), Mockito.any());
  }

  @Test
  void testCashoutReq_BetsAs_Null() {
    ReflectionTestUtils.setField(cashoutOfferService, "cashoutOfferReqSize", 4);
    cashoutOfferService.prepareCashoutReq(Collections.emptySet(), false);
    verify(betUpdatesTopic, times(0)).sendBetUpdate(Mockito.any(), Mockito.any());
  }

  @Test
  void testCashoutReq_Error() {
    try {
      cashoutOfferService.prepareCashoutReq(Collections.emptySet(), false);
    } catch (IllegalArgumentException e) {
      assertNotNull(e);
    }
  }

  @Test
  void testBetIdSubList() {
    ReflectionTestUtils.setField(cashoutOfferService, "betIdSize", 4);
    Set<String> betIds = new HashSet<>();
    betIds.add("23412312");
    betIds.add("23412311");
    betIds.add("23412314");
    List<List<String>> ids = cashoutOfferService.betIdSubList(betIds);
    assertEquals(1, ids.size());
  }

  @Test
  void testGetBetDetail() {
    List<Bet> bets = new ArrayList<>();
    Bet bet = new Bet();
    bet.setBetId("231465");
    bets.add(bet);
    GetBetDetailRequest getBetDetailRequest =
        GetBetDetailRequest.builder().betIds(Collections.singletonList("231465")).build();
    BetDetailRequestCtx betDetailRequestCtx =
        BetDetailRequestCtx.builder().request(getBetDetailRequest).build();
    cashoutOfferService.getBetDetail(betDetailRequestCtx);
  }

  private Set<BetSummaryModel> getBets(String fileName) {
    Type type =
        new TypeToken<Set<BetSummaryModel>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    Set<BetSummaryModel> bets = GsonUtil.fromJson(fileName, type);
    return bets;
  }
}
