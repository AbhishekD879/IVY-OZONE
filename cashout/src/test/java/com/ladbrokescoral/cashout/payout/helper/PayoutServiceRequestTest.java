package com.ladbrokescoral.cashout.payout.helper;

import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.google.common.reflect.TypeToken;
import com.ladbrokescoral.cashout.model.safbaf.Meta;
import com.ladbrokescoral.cashout.model.safbaf.Rule4;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.payout.PayoutContext;
import com.ladbrokescoral.cashout.payout.PayoutRequest;
import com.ladbrokescoral.cashout.payout.PayoutRequestFactory;
import com.ladbrokescoral.cashout.service.updates.pubsub.Publisher;
import com.ladbrokescoral.cashout.util.GsonUtil;
import java.lang.reflect.Type;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageHeaders;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {PayoutServiceRequest.class, Publisher.class})
@MockitoSettings(strictness = Strictness.LENIENT)
class PayoutServiceRequestTest {

  @Autowired private PayoutServiceRequest payoutServiceRequest;
  @Autowired private Publisher publisher;
  @MockBean private PayoutRequestFactory payoutRequestFactory;
  private Selection selection;

  @BeforeEach
  public void initEach() {
    List<String> betTypes = new ArrayList<>();
    betTypes.add("SGL");
    betTypes.add("ACCA");
    ReflectionTestUtils.setField(payoutServiceRequest, "supportedBetTypes", betTypes);
    selection = new Selection();
    selection.setSelectionKey(BigInteger.valueOf(193796721));
    selection.setResultCode("Void");
  }

  @Test
  void testPayoutContext() {
    PayoutContext payoutContext =
        payoutServiceRequest.buildPayoutContext(getBets("BetSummaryModel.json"), selection);
    assertEquals("2147633437", payoutContext.getVoidedBetsPotentialReturns().get(0).getBetId());
  }

  @Test
  void testPayoutContext_Non_BanachBets() {
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).setSource("I");
    when(payoutRequestFactory.buildPayoutRequest(Mockito.any(), Mockito.any()))
        .thenReturn(getReturns("PayoutRequest.json").get(0));
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(1, payoutContext.getPayoutRequests().size());
  }

  @Test
  void testPayoutContext_DeadHeatApplied() {
    List<BetSummaryModel> bets = getBets("BetSummaryModel7.json");
    bets.get(0).setSource("I");
    when(payoutRequestFactory.buildPayoutRequest(Mockito.any(), Mockito.any()))
        .thenReturn(getReturns("PayoutRequest.json").get(0));
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(0, payoutContext.getPayoutRequests().size());
  }

  @Test
  void testPayoutContext_Non_BanachBets_Rules4() {
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).getLeg().get(0).getPart().get(0).getDeduction().get(0).setValue("10");
    bets.get(0).setSource("I");
    when(payoutRequestFactory.buildPayoutRequest(Mockito.any(), Mockito.any()))
        .thenReturn(getReturns("PayoutRequest.json").get(0));
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(1, payoutContext.getPayoutRequests().size());
  }

  @Test
  void testPayoutContext_Forecast() {
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).getLeg().get(0).getPart().get(0).getDeduction().get(0).setValue("10");
    bets.get(0).setSource("I");
    bets.get(0).getLeg().get(0).getPart().get(0).getPrice().get(0).getPriceType().setCode("D");
    when(payoutRequestFactory.buildPayoutRequest(Mockito.any(), Mockito.any()))
        .thenReturn(getReturns("PayoutRequest.json").get(0));
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(1, payoutContext.getPayoutRequests().size());
  }

  @Test
  void testPayoutContext_BanachBets() {
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).getLeg().get(0).getPart().get(0).getOutcome().get(0).getResult().setValue("-");
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(0.0, payoutContext.getVoidedBetsPotentialReturns().get(0).getReturns(), 0);
  }

  @Test
  void testPayoutContext_Non_supportedBetTypes() {
    List<String> betTypes = new ArrayList<>();
    betTypes.add("Pxy");
    ReflectionTestUtils.setField(payoutServiceRequest, "supportedBetTypes", betTypes);
    selection.setResultCode("Lose");
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).getLeg().get(0).getPart().get(0).getOutcome().get(0).getResult().setValue("-");
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(Collections.emptyList(), payoutContext.getPayoutRequests());
  }

  @Test
  void testPayoutContext_ResultCode_Null() {
    selection.setResultCode(null);
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).getLeg().get(0).getPart().get(0).getOutcome().get(0).getResult().setValue("-");
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(Collections.emptyList(), payoutContext.getPayoutRequests());
  }

  @Test
  void testPayoutContext__Non_supportedBetTypes() {
    List<String> betTypes = new ArrayList<>();
    betTypes.add("Pxy");
    ReflectionTestUtils.setField(payoutServiceRequest, "supportedBetTypes", betTypes);
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).setSource("I");
    bets.get(0).getBetType().setCode("ACCA");
    bets.get(0).getLeg().get(0).getPart().get(0).getOutcome().get(0).getResult().setValue("-");
    PayoutContext payoutContext = payoutServiceRequest.buildPayoutContext(bets, selection);
    assertEquals(Collections.emptyList(), payoutContext.getPayoutRequests());
  }

  @Test
  void testPayoutRequests() {
    List<PayoutRequest> payoutReqs =
        payoutServiceRequest.buildPayoutRequests(getBets("BetSummaryModel.json"));
    assertEquals(Collections.emptyList(), payoutReqs);
  }

  @Test
  void testPayoutRequests_Non_BanachBets() {
    when(payoutRequestFactory.buildPayoutRequest(Mockito.any()))
        .thenReturn(getReturns("PayoutRequest.json").get(0));
    List<BetSummaryModel> bets = getBets("BetSummaryModel.json");
    bets.get(0).setSource("I");
    bets.get(0).getLeg().get(0).getPart().get(0).getDeduction().get(0).setType("deadheat");
    List<PayoutRequest> payoutReqs = payoutServiceRequest.buildPayoutRequests(bets);
    assertNotNull(payoutReqs);
    assertEquals(1, payoutReqs.size());
    assertEquals("ACCA", payoutReqs.get(0).getBetType());
  }

  @Test
  void testDeadHeatApplied() {
    boolean isDeadHeatApplied =
        payoutServiceRequest.isDeadHeatApplied(getBets("BetSummaryModel7.json").get(0));
    boolean isSpSelectionApplied =
        payoutServiceRequest.isSpSelection(getBets("BetSummaryModel7.json").get(0));
    boolean betElgibleForPayoutRequest =
        payoutServiceRequest.isBetElgibleForPayoutRequest(getBets("BetSummaryModel7.json").get(0));

    assertEquals(true, isDeadHeatApplied);
    assertEquals(true, isSpSelectionApplied);
    assertEquals(false, betElgibleForPayoutRequest);
  }

  @Test
  void testSpSelection() {
    boolean betElgibleForPayoutRequest =
        payoutServiceRequest.isBetElgibleForPayoutRequest(getBets("BetSummaryModel7.json").get(1));
    assertEquals(false, betElgibleForPayoutRequest);
  }

  @Test
  void testHandleMessage() {
    try {
      Message<Selection> msg =
          new Message<Selection>() {
            @Override
            public Selection getPayload() {
              Selection selection = new Selection();
              Rule4 rule4 = new Rule4();
              rule4.setRule4Id(49350814);
              rule4.setDeduction(2.3);
              Meta meta = new Meta();
              meta.setParents("c.21:cl.223:t.1892:e.3394569:m.49350814");
              selection.setMeta(meta);
              selection.setRule4(rule4);
              return selection;
            }

            @Override
            public MessageHeaders getHeaders() {
              return null;
            }
          };
      publisher.handleUpdateMessage(msg);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void testHandleMessage_rule4Null() {
    try {
      Message<Selection> msg =
          new Message<Selection>() {
            @Override
            public Selection getPayload() {
              Selection selection = new Selection();
              Meta meta = new Meta();
              meta.setParents("c.21:cl.223:t.1892:e.3394569:m.49350814");
              selection.setMeta(meta);
              return selection;
            }

            @Override
            public MessageHeaders getHeaders() {
              return null;
            }
          };
      publisher.handleUpdateMessage(msg);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void testHandleMessage_selKey() {
    try {
      Message<Selection> msg =
          new Message<Selection>() {
            @Override
            public Selection getPayload() {
              Selection selection = new Selection();
              Meta meta = new Meta();
              meta.setParents("c.21:cl.223:t.1892:e.3394569:m.49350814");
              selection.setMeta(meta);
              selection.setSelectionKey(BigInteger.valueOf(123456));
              return selection;
            }

            @Override
            public MessageHeaders getHeaders() {
              return null;
            }
          };
      publisher.handleUpdateMessage(msg);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  private List<BetSummaryModel> getBets(String fileName) {
    Type type =
        new TypeToken<List<BetSummaryModel>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    List<BetSummaryModel> bets = GsonUtil.fromJson(fileName, type);
    return bets;
  }

  private List<PayoutRequest> getReturns(String fileName) {
    Type type =
        new TypeToken<List<PayoutRequest>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    List<PayoutRequest> returns = GsonUtil.fromJson(fileName, type);
    return returns;
  }
}
