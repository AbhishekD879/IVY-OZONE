package com.egalacoral.spark.siteserver.api;

import java.util.List;
import org.joda.time.DateTime;
import org.junit.Assert;
import org.junit.Test;

public class SimpleFilterTest {

  @Test
  public void testSimpleFilter() {
    DateTime dt = new DateTime();

    SimpleFilter filter =
        new SimpleFilter.SimpleFilterBuilder() //
            .addField("f1") //
            .addUnaryOperation("f2", UnaryOperation.isTrue) //
            .addUnaryOperation("f3", UnaryOperation.isFalse) //
            .addUnaryOperation("f4", UnaryOperation.isEmpty) //
            .addUnaryOperation("f5", UnaryOperation.isNotEmpty) //
            .addBinaryOperation("f6", BinaryOperation.equals, 5) //
            .addBinaryOperation("f7", BinaryOperation.notEquals, "A") //
            .addBinaryOperation("f8", BinaryOperation.greaterThan, dt) //
            .addBinaryOperation("f9", BinaryOperation.lessThan, "B") //
            .build();

    List<String> queryMap = filter.getQueryMap();

    Assert.assertEquals(9, queryMap.size());

    Assert.assertEquals("f1", queryMap.get(0));
    Assert.assertEquals("f2:isTrue", queryMap.get(1));
    Assert.assertEquals("f3:isFalse", queryMap.get(2));
    Assert.assertEquals("f4:isEmpty", queryMap.get(3));
    Assert.assertEquals("f5:isNotEmpty", queryMap.get(4));
    Assert.assertEquals("f6:equals:5", queryMap.get(5));
    Assert.assertEquals("f7:notEquals:A", queryMap.get(6));
    Assert.assertEquals("f8:greaterThan:" + dt.toLocalDateTime().toString(), queryMap.get(7));
    Assert.assertEquals("f9:lessThan:B", queryMap.get(8));
  }
}
