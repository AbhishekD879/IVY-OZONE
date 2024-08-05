package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

/** Created by azayats on 08.05.17. */
public class BaseEventIdResolverTest {

  private BaseEventIdResolver idResolver;

  @Before
  public void setUp() {
    idResolver = new BaseEventIdResolver();
  }

  @After
  public void tearDown() {
    idResolver = null;
  }

  @Test
  public void test_sEVENT() throws Exception {
    long id = idResolver.resolveEventId("sEVENT0102030405");

    Assert.assertEquals(102030405, id);
  }

  @Test
  public void test_SEVENT() throws Exception {
    long id = idResolver.resolveEventId("SEVENT0000000005");

    Assert.assertEquals(5, id);
  }

  @Test
  public void test_sSCBRD() throws Exception {
    long id = idResolver.resolveEventId("sSCBRD1000000008");

    Assert.assertEquals(1000000008, id);
  }

  @Test(expected = NullPointerException.class)
  public void testNPE() throws Exception {
    idResolver.resolveEventId(null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testWrongId() throws Exception {
    idResolver.resolveEventId("sSCBRD10000000a8");
  }

  @Test(expected = IllegalArgumentException.class)
  public void testWrongType() throws Exception {
    idResolver.resolveEventId("sSOMES1000000008");
  }

  @Test(expected = ServiceException.class)
  public void testUnsupportedType() throws Exception {
    idResolver.resolveEventId("sEVMKT1000000008");
  }

  @Test
  public void testWhen16digitIdHasPadding() throws ServiceException {
    long eventId = idResolver.resolveEventId("sEVENT000000001051322108");
    Assert.assertEquals(1051322108, eventId);
  }

  @Test
  public void testLongIds() throws ServiceException {
    long eventId = idResolver.resolveEventId("sEVENT0000105132210809882");
    Assert.assertEquals(105132210809882L, eventId);
  }
}
