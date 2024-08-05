package com.coral.oxygen.middleware.ms.liveserv.utils;

import static org.junit.Assert.*;

import org.junit.Test;

public class LiveServeUtilTest {

  @Test
  public void testSubscriptionsCountIsCalculated() {
    String liveserverRequest =
        "CL0000S0003sCLOCK0010871239sEVENT0010133349sEVMKT0249269468S0001sSELCN0794295511!!!!l)A9QS0001sSELCN0796817452!!!!l)BI$S0001sSELCN0796817450!!!!l)A&<S0001sEVMKT0249556021!!!!l):+t";
    int count = LiveServeUtil.calculateSubscriptionCount(liveserverRequest);
    assertEquals(5, count);
  }

  @Test
  public void testCalculateWithOneSub() {
    String liveserverRequest = "CL0000S0003sCLOCK0010871239sEVENT0010133349sEVMKT0249269468";
    assertEquals(1, LiveServeUtil.calculateSubscriptionCount(liveserverRequest));
  }

  @Test
  public void testEmptySub() {
    String liveserverRequest = "";
    assertEquals(0, LiveServeUtil.calculateSubscriptionCount(liveserverRequest));
  }

  @Test
  public void testNull() {
    String liveserverRequest = null;
    assertEquals(0, LiveServeUtil.calculateSubscriptionCount(liveserverRequest));
  }
}
