package com.coral.oxygen.middleware.ms.liveserv.client;

import static com.coral.oxygen.middleware.ms.liveserv.utils.SubscriptionUtils.newSubscription;
import static com.coral.oxygen.middleware.ms.liveserv.utils.SubscriptionUtils.updatedSubscription;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.util.ArrayList;
import java.util.List;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

/** Created by azayats on 16.05.17. */
public class RequestBuilderTest {

  private RequestBuilder requestBuilder;
  private List<SubscriptionStats> subscriptions;

  @Before
  public void setUp() {
    subscriptions = new ArrayList<>();
    requestBuilder = new RequestBuilder();
  }

  @After
  public void tearDown() {
    requestBuilder = null;
    subscriptions = null;
  }

  @Test
  public void testOneNewSubscription() {
    // preparation
    subscriptions.add(newSubscription("sEVENT0102030405"));

    // action
    String result = requestBuilder.build(subscriptions);

    // verification
    Assert.assertEquals("CL0000S0001sEVENT0102030405!!!!!!!!!0", result);
  }

  @Test
  public void testTwoNewSubscriptions() {
    // preparation
    subscriptions.add(newSubscription("sEVENT0000000001"));
    subscriptions.add(newSubscription("sEVENT0000000002"));

    // action
    String result = requestBuilder.build(subscriptions);

    // verification
    Assert.assertEquals("CL0000S0002sEVENT0000000001sEVENT0000000002!!!!!!!!!0", result);
  }

  @Test
  public void testTwoUpdatedSubscriptions() {
    // preparation
    subscriptions.add(updatedSubscription("sEVENT0000000001", "15"));
    subscriptions.add(updatedSubscription("sEVENT0000000002", "20"));

    // action
    String result = requestBuilder.build(subscriptions);

    // verification
    Assert.assertEquals(
        "CL0000S0001sEVENT0000000001!!!!!!!!15S0001sEVENT0000000002!!!!!!!!20", result);
  }

  @Test
  public void testMixedSubscriptions() {
    // preparation
    subscriptions.add(newSubscription("sEVENT0000000003"));
    subscriptions.add(newSubscription("sEVENT0000000004"));
    subscriptions.add(updatedSubscription("sEVENT0000000001", "15"));
    subscriptions.add(updatedSubscription("sEVENT0000000002", "20"));

    // action
    String result = requestBuilder.build(subscriptions);

    // verification
    Assert.assertEquals(
        "CL0000S0002sEVENT0000000003sEVENT0000000004!!!!!!!!!0S0001sEVENT0000000001!!!!!!!!15S0001sEVENT0000000002!!!!!!!!20",
        result);
  }

  /** Not sure. Maybe it is better to throw exception in this case */
  @Test
  public void testZeroSubscriptions() {
    // preparation
    subscriptions.clear();

    // action
    String result = requestBuilder.build(subscriptions);

    // verification
    Assert.assertEquals("CL0000", result);
  }

  @Test
  public void test9999NewSubscriptions() {
    // preparation
    int count = 9999;
    for (int i = 1; i <= count; i++) {
      subscriptions.add(newSubscription("sEVENT" + String.format("%010d", i)));
    }

    // action
    String result = requestBuilder.build(subscriptions);

    // verification
    int expectedLenght =
        6 // CL0000
            + 5 // S9999
            + 16 * count // sEVENT + 10 ID
            + 10; // wark

    Assert.assertEquals(expectedLenght, result.length());
    Assert.assertEquals(
        "Starts with", "CL0000S9999sEVENT0000000001sEVENT0000000002", result.substring(0, 43));
    Assert.assertEquals(
        "Ends with",
        "sEVENT0000009998sEVENT0000009999!!!!!!!!!0",
        result.substring(result.length() - 42));
  }

  @Test
  public void test20000NewSubscriptions() {
    // preparation
    int count = 20000;
    for (int i = 1; i <= count; i++) {
      subscriptions.add(newSubscription("sEVENT" + String.format("%010d", i)));
    }

    // action
    String result = requestBuilder.build(subscriptions);

    // verification
    int expectedLenght =
        6 // CL0000
            + 5 * 3 // S9999 (3 chunks 9999 + 9999 + 2)
            + 16 * count // sEVENT + 10 ID
            + 10 * 3; // wark (3 chunks 9999 + 9999 + 2)

    Assert.assertEquals(expectedLenght, result.length());
    Assert.assertEquals(
        "Starts with", "CL0000S9999sEVENT0000000001sEVENT0000000002", result.substring(0, 43));
    Assert.assertEquals(
        "Ends with",
        "S0002sEVENT0000019999sEVENT0000020000!!!!!!!!!0",
        result.substring(result.length() - 47));
  }
}
