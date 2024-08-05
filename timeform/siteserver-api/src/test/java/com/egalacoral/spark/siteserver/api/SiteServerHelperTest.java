package com.egalacoral.spark.siteserver.api;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;

public class SiteServerHelperTest {

  @Test
  public void testCall() {
    List<Integer> data = Arrays.asList(1, 2, 3, 4, 5);
    Optional<List<String>> output =
        SiteServerAPI.pagedCalls(data, 2, pagedInput -> loadData(pagedInput));
    Assert.assertEquals(9, output.get().size());
  }

  public Optional<List<String>> loadData(List<Integer> input) {
    return Optional.of(Arrays.asList("1", "2", "3"));
  }
}
