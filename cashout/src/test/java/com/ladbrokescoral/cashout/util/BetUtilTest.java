package com.ladbrokescoral.cashout.util;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.coral.bpp.api.model.bet.api.response.accountHistory.Paging;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.*;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class BetUtilTest {

  @Test
  void testBetCashoutAvailable() {
    Bet bet = new Bet();
    boolean result = BetUtil.isBetCashoutAvailable(bet);
    assertFalse(result);

    bet.setCashoutValue("1.2");
    result = BetUtil.isBetCashoutAvailable(bet);
    assertTrue(result);

    bet.setCashoutValue("");
    result = BetUtil.isBetCashoutAvailable(bet);
    assertFalse(result);

    bet.setCashoutValue("sashout not avaiable");
    result = BetUtil.isBetCashoutAvailable(bet);
    assertFalse(result);
  }

  @Test
  void testIsBanachTest() {
    Bet bet = new Bet();
    bet.setSource("e");

    Bet bet2 = new Bet();
    bet2.setSource("f");

    Bet bet3 = new Bet();
    bet3.setSource("M");

    assertTrue(BetUtil.isBanachBet(bet));
    assertTrue(BetUtil.isBanachBet(bet2));
    assertFalse(BetUtil.isBanachBet(bet3));
  }

  @Test
  void testFilterAccHistoryBetsWithCashoutValuePresent() {
    List<BetSummaryModel> betSummaryModelList =
        BetUtil.filterAccHistoryBetsWithCashoutValuePresent(accountHistoryResponse());
    Assertions.assertEquals(2, betSummaryModelList.size());
  }

  @Test
  void testIsBetOnLPPrice() {
    BetSummaryModel bet = betSummaryLPObjResp();
    boolean flag = BetUtil.isBetOnLPPrice(bet, BigInteger.valueOf(693379));
    assertTrue(flag);
  }

  @Test
  void testIsBetOnGPPrice() {
    BetSummaryModel bet = betSummaryGPObjResp();
    boolean flag = BetUtil.isBetOnLPPrice(bet, BigInteger.valueOf(235678));
    assertTrue(flag);
  }

  @Test
  void testIsBetOnEmptyPriceTypeCode() {
    BetSummaryModel bet = betSummaryEmtptyTypeCodeObjResp();
    boolean flag = BetUtil.isBetOnLPPrice(bet, BigInteger.valueOf(235678));
    assertFalse(flag);
  }

  @Test
  void testIsBetOnEmptyPriceType() {
    BetSummaryModel bet = betSummaryEmptyTypeObjResp();
    boolean flag = BetUtil.isBetOnLPPrice(bet, BigInteger.valueOf(235678));
    assertFalse(flag);
  }

  private static BetSummaryModel betSummaryEmptyTypeObjResp() {
    BetSummaryModel betSummaryModel = new BetSummaryModel();
    List<Leg> legList = new ArrayList<>();
    List<Part> partList = new ArrayList<>();
    List<Outcome> outcomeList = new ArrayList<>();
    List<Price> priceList = new ArrayList<>();
    Leg leg = new Leg();
    Outcome outcome = new Outcome();
    Part part = new Part();
    Price price = new Price();
    outcome.setId("235678");
    outcomeList.add(outcome);
    part.setOutcome(outcomeList);
    priceList.add(price);
    part.setPrice(priceList);
    partList.add(part);
    leg.setPart(partList);
    legList.add(leg);
    betSummaryModel.setLeg(legList);
    return betSummaryModel;
  }

  private static BetSummaryModel betSummaryEmtptyTypeCodeObjResp() {
    BetSummaryModel betSummaryModel = new BetSummaryModel();
    List<Leg> legList = new ArrayList<>();
    List<Part> partList = new ArrayList<>();
    List<Outcome> outcomeList = new ArrayList<>();
    List<Price> priceList = new ArrayList<>();
    Leg leg = new Leg();
    Outcome outcome = new Outcome();
    Part part = new Part();
    Price price = new Price();
    Code code = new Code();
    outcome.setId("235678");
    outcomeList.add(outcome);
    part.setOutcome(outcomeList);
    price.setPriceType(code);
    priceList.add(price);
    part.setPrice(priceList);
    partList.add(part);
    leg.setPart(partList);
    legList.add(leg);
    betSummaryModel.setLeg(legList);
    return betSummaryModel;
  }

  private static BetSummaryModel betSummaryGPObjResp() {
    BetSummaryModel betSummaryModel = new BetSummaryModel();
    List<Leg> legList = new ArrayList<>();
    List<Part> partList = new ArrayList<>();
    List<Outcome> outcomeList = new ArrayList<>();
    List<Price> priceList = new ArrayList<>();
    Leg leg = new Leg();
    Outcome outcome = new Outcome();
    Part part = new Part();
    Price price = new Price();
    Code code = new Code();
    outcome.setId("235678");
    outcomeList.add(outcome);
    part.setOutcome(outcomeList);
    code.setCode("G");
    price.setPriceType(code);
    priceList.add(price);
    part.setPrice(priceList);
    partList.add(part);
    leg.setPart(partList);
    legList.add(leg);
    betSummaryModel.setLeg(legList);
    return betSummaryModel;
  }

  private static BetSummaryModel betSummaryLPObjResp() {
    BetSummaryModel betSummaryModel = new BetSummaryModel();
    List<Leg> legList = new ArrayList<>();
    List<Part> partList = new ArrayList<>();
    List<Outcome> outcomeList = new ArrayList<>();
    List<Price> priceList = new ArrayList<>();
    Leg leg = new Leg();
    Outcome outcome = new Outcome();
    Part part = new Part();
    Price price = new Price();
    Code code = new Code();
    outcome.setId("693379");
    outcomeList.add(outcome);
    part.setOutcome(outcomeList);
    code.setCode("L");
    price.setPriceType(code);
    priceList.add(price);
    part.setPrice(priceList);
    partList.add(part);
    leg.setPart(partList);
    legList.add(leg);
    betSummaryModel.setLeg(legList);
    return betSummaryModel;
  }

  private static InitialAccountHistoryBetResponse accountHistoryResponse() {
    List<BetSummaryModel> betList = new ArrayList<>();
    BetSummaryModel model1 = new BetSummaryModel();
    List<Leg> legList1 = new ArrayList<>();
    List<Part> partList1 = new ArrayList<>();
    List<Outcome> outcomeList1 = new ArrayList<>();
    Leg leg1 = new Leg();
    Outcome outcome1 = new Outcome();
    Part part1 = new Part();
    IdName idName1 = new IdName();
    idName1.setId("16");
    idName1.setName("Football");
    outcome1.setEventCategory(idName1);
    outcomeList1.add(outcome1);
    part1.setOutcome(outcomeList1);
    partList1.add(part1);
    leg1.setPart(partList1);
    legList1.add(leg1);
    model1.setLeg(legList1);
    model1.setId("693379");
    model1.setCashoutValue("CASHOUT_SELN_NO_CASHOUT");

    BetSummaryModel model2 = new BetSummaryModel();
    List<Leg> legList = new ArrayList<>();
    List<Part> partList = new ArrayList<>();
    List<Outcome> outcomeList = new ArrayList<>();
    Leg leg = new Leg();
    Outcome outcome = new Outcome();
    Part part = new Part();
    IdName idName = new IdName();

    idName.setId("21");
    idName.setName("Horse Racing");
    outcome.setEventCategory(idName);
    outcomeList.add(outcome);
    part.setOutcome(outcomeList);
    partList.add(part);
    leg.setPart(partList);
    legList.add(leg);
    model2.setLeg(legList);
    model2.setId("693378");
    model2.setCashoutValue("CASHOUT_SELN_NO_CASHOUT");

    BetSummaryModel model3 = new BetSummaryModel();
    model3.setId("693378");
    model3.setCashoutValue("CASHOUT_SELN_SUSPENDED");

    betList.add(model1);
    betList.add(model2);
    betList.add(model3);

    Paging paging = new Paging();
    paging.setToken("abc");
    paging.setBlockSize("20");

    return new InitialAccountHistoryBetResponse(betList, null, null, paging, "abc", "1");
  }
}
