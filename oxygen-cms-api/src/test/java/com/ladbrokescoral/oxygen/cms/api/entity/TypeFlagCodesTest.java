package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TypeFlagCodesTest {

  @Test
  public void testOfNull() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of((String) null);
    List<String> codes = typeFlagCodes.getCodes();
    Assert.assertNotNull(codes);
  }

  @Test
  public void testOfString() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire,uk,int");
    List<String> codes = typeFlagCodes.getCodes();
    Assert.assertNotNull(codes);
    Assert.assertEquals(3, codes.size());
    Assert.assertEquals("ire", codes.get(0));
    Assert.assertEquals("uk", codes.get(1));
    Assert.assertEquals("int", codes.get(2));
  }

  @Test
  public void testOfStringComman() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire,uk,int,");
    List<String> codes = typeFlagCodes.getCodes();
    Assert.assertNotNull(codes);
    Assert.assertEquals(3, codes.size());
    Assert.assertEquals("ire", codes.get(0));
    Assert.assertEquals("uk", codes.get(1));
    Assert.assertEquals("int", codes.get(2));
  }

  @Test
  public void testOfArray() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    List<String> codes = typeFlagCodes.getCodes();
    Assert.assertNotNull(codes);
    Assert.assertEquals(3, codes.size());
    Assert.assertEquals("ire", codes.get(0));
    Assert.assertEquals("uk", codes.get(1));
    Assert.assertEquals("int", codes.get(2));
  }

  @Test
  public void testToString() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    Assert.assertEquals(typeFlagCodes.toString(), "ire,uk,int");
  }

  @Test
  public void contains() {
    TypeFlagCodes sourceTypeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    TypeFlagCodes gbrTypeFlagCodes = TypeFlagCodes.of("ire", "uk");
    Assert.assertTrue(sourceTypeFlagCodes.contains(gbrTypeFlagCodes));

    TypeFlagCodes sourceIreTypeFlagCodes = TypeFlagCodes.of("ire");
    Assert.assertTrue(sourceIreTypeFlagCodes.contains(gbrTypeFlagCodes));
  }
}
