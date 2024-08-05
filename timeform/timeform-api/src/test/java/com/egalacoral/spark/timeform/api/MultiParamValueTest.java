package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.services.endpoints.params.MultiParamValue;
import java.util.Arrays;
import org.junit.Assert;
import org.junit.Test;

public class MultiParamValueTest {

  @Test
  public void testMultiParamsBuild() {
    MultiParamValue multiParamValue =
        new MultiParamValue("greyhound_id eq %s", Arrays.asList(1, 2, 3, 4, 5));
    String result = multiParamValue.build();
    Assert.assertEquals(
        "(greyhound_id eq 1 or greyhound_id eq 2 or greyhound_id eq 3 or greyhound_id eq 4 or greyhound_id eq 5)",
        result);
  }
}
