package com.egalacoral.spark.timeform.rql;

import com.egalacoral.spark.timeform.gson.GsonUKDateAdapter;
import com.egalacoral.spark.timeform.model.greyhound.Performance;
import java.text.ParseException;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class QueryStreamTest {

  private GsonUKDateAdapter adapter;
  private List<Performance> performances;
  private Performance performance2;
  private Performance performance1;

  @Before
  public void init() throws ParseException {
    adapter = new GsonUKDateAdapter();

    Performance performance0 = new Performance();
    performance0.setPerformanceId(1);
    performance0.setExpSecTime(7.0);
    performance0.setUpdateDate(new Date());
    performance0.setGreyhoundFullName("test1");
    performance0.setBendPositions("01000000001000000.0000");
    performance1 = new Performance();
    performance1.setPerformanceId(100);
    performance1.setExpSecTime(2.0);
    performance1.setUpdateDate(adapter.getDateFormat().parse("2014-09-04T13:26:54+0100"));
    performance1.setGreyhoundFullName("test2");
    performance2 = createPerfomance("test2");

    Date parse = adapter.getDateFormat().parse("2016-09-04T13:26:54+0100");
    performance2.setUpdateDate(parse);
    System.out.println(parse);

    Performance performance4 = createPerfomance("test4(t)");
    performance4.setUpdateDate(new Date(0));
    performances = Arrays.asList(performance0, performance1, performance2, performance4);
  }

  protected Performance createPerfomance(String name) {
    Performance performance = new Performance();
    performance.setPerformanceId(80);
    performance.setGreyhoundFullName(name);
    performance.setExpSecTime(20.0);
    performance.setBendPositions("00000000001000000");
    return performance;
  }

  @Test
  public void testFilterDate() throws ParseException {
    Date parse = adapter.getDateFormat().parse("2016-09-04T13:26:54+0100");
    String dates = adapter.getDateFormat().format(parse);
    QueryStream<Performance> dataStream = QueryStream.of(performances, "updateDate=" + dates);
    Assert.assertEquals(1, dataStream.stream().count());
  }

  @Test
  public void testFilterYear() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, "updateDate>2015");
    Assert.assertEquals(2, dataStream.stream().count());
  }

  @Test
  public void testFilteOrderByAsc() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, null, "+expSecTime");
    Assert.assertEquals(4, dataStream.stream().count());
    Assert.assertEquals(performance1, dataStream.stream().toArray()[0]);
  }

  @Test
  public void testFilteOrderByDesc() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, null, "-expSecTime");
    Assert.assertEquals(4, dataStream.stream().count());
    Assert.assertEquals(performance2, dataStream.stream().toArray()[0]);
  }

  @Test
  public void testTopN() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, null, null, 2, null);
    Assert.assertEquals(2, dataStream.stream().count());
  }

  @Test
  public void testStartN() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, null, null, null, 2);
    Assert.assertEquals(2, dataStream.stream().count());
    Assert.assertEquals(performance2, dataStream.stream().toArray()[0]);
  }

  @Test
  public void testTopNstartN() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, null, null, 1, 2);
    Assert.assertEquals(1, dataStream.stream().count());
  }

  @Test
  public void testCompareDifferentTypes() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, "expSecTime>2");
    Assert.assertEquals(3, dataStream.stream().count());
  }

  @Test(expected = UnsupportedOperationException.class)
  public void testInvalidOrderByFormat() throws ParseException {
    QueryStream.of(performances, "expSecTime");
  }

  @Test(expected = UnsupportedOperationException.class)
  public void testInvalidSortField() throws ParseException {
    QueryStream.of(performances, "-expSecTime1");
  }

  @Test
  public void testMatch() throws ParseException {
    QueryStream<Performance> dataStream =
        QueryStream.of(performances, "match(greyhoundFullName,*st4*)");
    Assert.assertEquals(1, dataStream.stream().count());
  }

  @Test
  public void testLogical() throws ParseException {
    QueryStream<Performance> dataStream =
        QueryStream.of(
            performances, "(expSecTime>2|match(greyhoundFullName,*st4))&updateDate>2015");
    Assert.assertEquals(2, dataStream.stream().count());
  }

  @Test
  public void testLargeNumbers() throws ParseException {
    QueryStream<Performance> dataStream =
        QueryStream.of(performances, "bendPositions=00000000001000000");
    Assert.assertEquals(2, dataStream.stream().count());

    dataStream = QueryStream.of(performances, "bendPositions=01000000001000000.0000");
    Assert.assertEquals(1, dataStream.stream().count());
  }

  @Test
  public void testNumber() throws ParseException {
    QueryStream<Performance> dataStream = QueryStream.of(performances, "expSecTime=2");
    Assert.assertEquals(1, dataStream.stream().count());

    dataStream = QueryStream.of(performances, "expSecTime=2.000");
    Assert.assertEquals(1, dataStream.stream().count());
  }
}
