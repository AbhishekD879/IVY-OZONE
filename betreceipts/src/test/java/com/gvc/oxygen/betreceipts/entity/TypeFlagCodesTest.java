package com.gvc.oxygen.betreceipts.entity;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.util.Arrays;
import java.util.List;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Test;

public class TypeFlagCodesTest implements WithAssertions {

  @Test
  public void testOfNull() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of((String) null);
    List<String> codes = typeFlagCodes.getCodes();
    assertNotNull(codes);
  }

  @Test
  public void testOfString() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire,uk,int");
    List<String> codes = typeFlagCodes.getCodes();
    assertThat(codes).isNotNull().hasSize(3).containsAll(Arrays.asList("ire", "uk", "int"));
  }

  @Test
  public void testOfStringComman() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire,uk,int,");
    List<String> codes = typeFlagCodes.getCodes();
    assertThat(codes).isNotNull().hasSize(3).containsAll(Arrays.asList("ire", "uk", "int"));
  }

  @Test
  public void testOfArray() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    List<String> codes = typeFlagCodes.getCodes();
    assertThat(codes).isNotNull().hasSize(3).containsAll(Arrays.asList("ire", "uk", "int"));
  }

  @Test
  public void testToString() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    assertThat(typeFlagCodes.toString()).isEqualTo("ire,uk,int");
  }

  @Test
  public void contains() {
    TypeFlagCodes sourceTypeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    TypeFlagCodes gbrTypeFlagCodes = TypeFlagCodes.of("ire", "uk");
    assertThat(sourceTypeFlagCodes.contains(gbrTypeFlagCodes)).isTrue();

    TypeFlagCodes sourceIreTypeFlagCodes = TypeFlagCodes.of("ire");
    assertThat(sourceIreTypeFlagCodes.contains(gbrTypeFlagCodes)).isTrue();
  }

  @Test
  public void testHashcode() {
    TypeFlagCodes sourceTypeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    int hashCode = sourceTypeFlagCodes.hashCode();
    assertThat(sourceTypeFlagCodes.hashCode()).isEqualTo(hashCode);
  }

  @Test
  public void testEquals() {
    TypeFlagCodes typeFlagCodes = TypeFlagCodes.of((String) null);
    TypeFlagCodes sourceTypeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    assertThat(sourceTypeFlagCodes.equals(typeFlagCodes)).isFalse();
    assertThat(sourceTypeFlagCodes.equals(new String(""))).isFalse();
  }

  @Test
  public void testEqualsForSame() {
    TypeFlagCodes sourceTypeFlagCodes = TypeFlagCodes.of("ire", "uk", "int");
    assertThat(sourceTypeFlagCodes.equals(sourceTypeFlagCodes)).isTrue();
    assertThat(sourceTypeFlagCodes.equals(null)).isFalse();
  }
}
