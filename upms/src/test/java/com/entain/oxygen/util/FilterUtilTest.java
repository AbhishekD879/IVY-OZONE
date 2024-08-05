package com.entain.oxygen.util;

import static org.junit.jupiter.api.Assertions.*;

import com.egalacoral.spark.siteserver.api.*;
import org.junit.jupiter.api.Test;

class FilterUtilTest {

  @Test
  void testBuildSimpleFilterForUKIEHorsesNotNull() {
    SimpleFilter simpleFilter = (SimpleFilter) FilterUtil.buildSimpleFilterForUKIEHorses().build();
    assertNotNull(simpleFilter);
  }

  @Test
  void testLimitToFilterNotNull() {
    LimitToFilter limitToFilter = FilterUtil.limitToFilter();
    assertNotNull(limitToFilter);
  }
}
