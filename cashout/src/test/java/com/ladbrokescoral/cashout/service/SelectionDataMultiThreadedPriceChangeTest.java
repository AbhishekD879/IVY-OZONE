package com.ladbrokescoral.cashout.service;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Code;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price;
import com.google.testing.threadtester.AnnotatedTestRunner;
import com.google.testing.threadtester.ThreadedAfter;
import com.google.testing.threadtester.ThreadedBefore;
import com.google.testing.threadtester.ThreadedMain;
import com.google.testing.threadtester.ThreadedSecondary;
import java.math.BigInteger;
import java.util.Collections;
import org.junit.jupiter.api.Test;

public class SelectionDataMultiThreadedPriceChangeTest {
  private SelectionData selectionData;

  @ThreadedBefore
  public void before() {
    selectionData =
        new SelectionData(BigInteger.valueOf(1), BigInteger.valueOf(2), BigInteger.valueOf(3));
    Part part = new Part();
    Price price = new Price();
    price.setCurrentPriceNum("1");
    price.setCurrentPriceNum("2");
    Code priceType = new Code();
    priceType.setCode("L");
    price.setPriceType(priceType);
    part.setPrice(Collections.singletonList(price));
    selectionData.getParts().add(part);
    selectionData.changeLpPrice(1, 2);
  }

  @ThreadedMain
  public void mainThread() {
    selectionData.changeLpPrice(2, 3);
  }

  @ThreadedSecondary
  public void secondThread() {
    selectionData.changeLpPrice(3, 4);
  }

  @ThreadedAfter
  public void after() {
    SelectionDataPrice priceInModel = selectionData.getLpPrice().get();
    Price priceInBet = selectionData.getParts().get(0).getPrice().get(0);
    assertEquals(priceInBet.getCurrentPriceNum(), String.valueOf(priceInModel.getNum()));
    assertEquals(priceInBet.getCurrentPriceDen(), String.valueOf(priceInModel.getDen()));
  }

  @Test
  public void testConcurrentPriceModification() {
    AnnotatedTestRunner runner = new AnnotatedTestRunner();
    runner.runTests(this.getClass(), SelectionData.class);
  }
}
