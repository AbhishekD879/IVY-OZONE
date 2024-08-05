package com.coral.siteserver.api;

import java.util.List;
import org.junit.Assert;
import org.junit.Test;

public class SimpleFilterTest {

  @Test
  public void testSimpleFilter() {
    SimpleFilter filter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addHasPricestream("hasPriceStream", "isTrue", true)
                .addHasPricestream("hasPriceStream", "isTrue", false)
                .build();

    List<String> queryMap = filter.getQueryMap();
    Assert.assertEquals("hasPriceStream:isTrue", queryMap.get(0));
  }
}
