package com.ladbrokescoral.cashout.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.google.testing.threadtester.AnnotatedTestRunner;
import com.google.testing.threadtester.ThreadedAfter;
import com.google.testing.threadtester.ThreadedBefore;
import com.google.testing.threadtester.ThreadedMain;
import com.google.testing.threadtester.ThreadedSecondary;
import com.ladbrokescoral.cashout.service.SelectionData.SelectionStatus;
import java.math.BigInteger;
import org.junit.jupiter.api.Test;

public class SelectionDataMultithreadedStatusChangeTest {

  private SelectionData selectionData;
  private volatile boolean t1Result = false;
  private volatile boolean t2Result = false;

  @ThreadedBefore
  public void before() {
    selectionData =
        new SelectionData(BigInteger.valueOf(1), BigInteger.valueOf(2), BigInteger.valueOf(3));
    selectionData.changeEventStatus(true);
    selectionData.changeMarketStatus(true);
    selectionData.changeSelectionStatus(false);
  }

  @ThreadedMain
  public void mainThread() {
    selectionData.changeMarketStatus(true);
    t1Result = selectionData.changeSelectionStatus(true);
  }

  @ThreadedSecondary
  public void secondThread() {
    selectionData.changeMarketStatus(true);
    t2Result = selectionData.changeSelectionStatus(true);
  }

  @ThreadedAfter
  public void after() {
    assertEquals(SelectionStatus.ACTIVE, selectionData.getSelectionStatus());
    assertTrue(selectionData.getEventActive());
    assertTrue(selectionData.getMarketActive());
    assertTrue(selectionData.getSelectionActive());
    System.out.println(t1Result);
    System.out.println(t2Result);
    assertTrue(t1Result ^ t2Result);
  }

  @Test
  public void testConcurrentPriceModification() {
    AnnotatedTestRunner runner = new AnnotatedTestRunner();
    runner.runTests(this.getClass(), SelectionData.class);
  }
}
