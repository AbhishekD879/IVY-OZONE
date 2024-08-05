package com.oxygen.publisher.sportsfeatured.context;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertSame;

import org.junit.Test;

public class ClientTypeTest {

  @Test
  public void shouldCreateClientTypeFromTypeString() {
    ClientType ios = ClientType.from("ios");
    ClientType android = ClientType.from("android");
    ClientType wp = ClientType.from("wp");
    ClientType web = ClientType.from(null);

    assertSame(ClientType.IOS, ios);
    assertSame(ClientType.ANDROID, android);
    assertSame(ClientType.WP, wp);
    assertSame(ClientType.WEB, web);

    assertEquals(ClientType.IOS.getTypeInUrlForm(), "/ios");
    assertEquals(ClientType.ANDROID.getTypeInUrlForm(), "/android");
    assertEquals(ClientType.WP.getTypeInUrlForm(), "/wp");
    assertEquals(ClientType.WEB.getTypeInUrlForm(), "");
  }

  @Test(expected = IllegalArgumentException.class)
  public void shouldThrowWhenInvalidClientType() {
    ClientType.from("iphone");
  }
}
