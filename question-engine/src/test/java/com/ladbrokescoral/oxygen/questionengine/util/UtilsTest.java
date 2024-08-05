package com.ladbrokescoral.oxygen.questionengine.util;

import org.junit.Test;

import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class UtilsTest {

  @Test
  public void splitIntoBatches() {
    List<String> ids = Arrays.asList("1", "2", "3", "4", "5", "6");
    Collection<? extends Collection<String>> splitIds = Utils.splitIntoBatches(ids, 3);

    assertEquals(2, splitIds.size());
  }

  @Test
  public void toAlphabeticRepresentationSingleLetter() {
    assertEquals("Z", Utils.toAlphabeticRepresentation(25));
  }

  @Test
  public void toAlphabeticRepresentationDoubleLetter() {
    assertEquals("AB", Utils.toAlphabeticRepresentation(26));
  }

  @Test
  public void toAlphabeticRepresentationTripleLetter() {
    assertEquals("AAD", Utils.toAlphabeticRepresentation(53));
  }

  @Test(expected = IllegalArgumentException.class)
  public void toAlphabeticRepresentationNegativeNumber() {
    Utils.toAlphabeticRepresentation(-1);
  }
}
