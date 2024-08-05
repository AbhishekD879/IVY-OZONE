package com.oxygen.publisher.model;

import static org.junit.Assert.assertEquals;

import org.junit.Ignore;
import org.junit.Test;

/** Created by Aliaksei Yarotski on 4/13/18. */
@Deprecated
@Ignore
public class RawIndexTest {

  @Test
  public void compareToLeftLowerByType() throws Exception {
    RawIndex left =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("UPCOMING_EVENT")
            .marketSelector("HH")
            .typeId(1111)
            .build();
    RawIndex right =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("UPCOMING_EVENT")
            .marketSelector("HH")
            .build();
    assertEquals(left.compareTo(right), -1);
    assertEquals(right.compareTo(left), 1);
  }

  @Test
  public void compareToLeftLowerByMarket() throws Exception {
    RawIndex left =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("UPCOMING_EVENT")
            .marketSelector("HH")
            .typeId(1111)
            .build();
    RawIndex right =
        RawIndex.builder().categoryId(16).topLevelType("UPCOMING_EVENT").typeId(2222).build();
    assertEquals(left.compareTo(right), -1);
    assertEquals(right.compareTo(left), 1);
  }

  @Test
  public void compareEqualsOnType() throws Exception {
    RawIndex left =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("UPCOMING_EVENT")
            .marketSelector("HH")
            .build();
    RawIndex right =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("UPCOMING_EVENT")
            .marketSelector("wwqwwq")
            .build();
    assertEquals(left.compareTo(right), 0);
    assertEquals(right.compareTo(left), 0);
  }

  @Test
  public void compareEqualsOnMarket() throws Exception {
    RawIndex left =
        RawIndex.builder().categoryId(16).topLevelType("UPCOMING_EVENT").typeId(2343).build();
    RawIndex right =
        RawIndex.builder().categoryId(16).topLevelType("UPCOMING_EVENT").typeId(123).build();
    assertEquals(left.compareTo(right), 0);
    assertEquals(right.compareTo(left), 0);
  }

  @Test
  public void compareEqualsByReqFields() throws Exception {
    RawIndex left = RawIndex.builder().categoryId(16).topLevelType("LIVE").build();
    RawIndex right = RawIndex.builder().categoryId(16).topLevelType("UPCOMING_EVENT").build();
    assertEquals(left.compareTo(right), 0);
    assertEquals(right.compareTo(left), 0);
  }

  @Test
  public void compareEqualsFull() throws Exception {
    RawIndex left =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("LIVE")
            .typeId(12)
            .marketSelector("ds")
            .build();
    RawIndex right =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("UPCOMING_EVENT")
            .typeId(934)
            .marketSelector("sfd")
            .build();
    assertEquals(left.compareTo(right), 0);
    assertEquals(right.compareTo(left), 0);
  }

  @Test
  public void compareLeftFull() throws Exception {
    RawIndex left =
        RawIndex.builder().categoryId(16).topLevelType("LIVE").marketSelector("ds").build();
    RawIndex right =
        RawIndex.builder()
            .categoryId(16)
            .topLevelType("UPCOMING_EVENT")
            .typeId(934)
            .marketSelector("sfd")
            .build();
    assertEquals(left.compareTo(right), 1);
    assertEquals(right.compareTo(left), -1);
  }
}
