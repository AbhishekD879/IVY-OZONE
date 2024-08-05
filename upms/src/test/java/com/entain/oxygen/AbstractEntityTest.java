package com.entain.oxygen;

import com.entain.oxygen.entity.AbstractEntity;
import com.entain.oxygen.entity.UserPreference;
import com.mongodb.assertions.Assertions;
import org.junit.jupiter.api.Test;

class AbstractEntityTest {

  private AbstractEntity abstractEntity = new UserPreference();

  @Test
  void testForFalseIsNew() {
    abstractEntity.setId(null);
    boolean value = abstractEntity.isNew();
    Assertions.assertTrue(true);
  }

  @Test
  void testForTrueIsNew() {
    abstractEntity.setId("123");
    boolean value = abstractEntity.isNew();
    Assertions.assertFalse(false);
  }
}
