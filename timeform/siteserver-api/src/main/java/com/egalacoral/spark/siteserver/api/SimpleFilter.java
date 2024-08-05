package com.egalacoral.spark.siteserver.api;

import java.util.LinkedList;
import java.util.List;
import org.joda.time.DateTime;

/**
 * Created by oleg.perushko@symphony-solutions.eu on 8/2/16
 *
 * <p>Many requests allow the client to specify that Records should be included in the response only
 * if they satisfy some client-supplied conditions, known as SimpleFilters. The client may do this
 * by supplying one or more "simpleFilter" query parameters. A SimpleFilter operates on all Records
 * of a particular RecordType (e.g. all the Event records considered for inclusion in the response)
 * and any Records that do not satisfy the SimpleFilter are discarded - that is, they are not
 * included in the response. Clients can supply multiple SimpleFilters, but there is no support for
 * constructing nested expressions from them - instead, if multiple SimpleFilters are given for the
 * same eld of a record, then the record is returned only if the record satis es all the
 * SimpleFilters given.
 */
public class SimpleFilter {

  private final List<String> queryMap;
  private static final String SEPARATOR = ":";

  private SimpleFilter(SimpleFilterBuilder builder) {
    queryMap = builder.queryMap;
  }

  public static class SimpleFilterBuilder {

    private final List<String> queryMap = new LinkedList<>();

    public SimpleFilterBuilder addField(String field) {
      queryMap.add(field);
      return this;
    }

    public SimpleFilterBuilder addUnaryOperation(String field, UnaryOperation operation) {
      queryMap.add(field + SEPARATOR + operation);
      return this;
    }

    public SimpleFilterBuilder addBinaryOperation(
        String field, BinaryOperation operation, Integer value) {
      queryMap.add(field + SEPARATOR + operation + SEPARATOR + value);
      return this;
    }

    public SimpleFilterBuilder addBinaryOperation(
        String field, BinaryOperation operation, String value) {
      queryMap.add(field + SEPARATOR + operation + SEPARATOR + value);
      return this;
    }

    public SimpleFilterBuilder addBinaryOperation(
        String field, BinaryOperation operation, DateTime value) {
      queryMap.add(field + SEPARATOR + operation + SEPARATOR + value.toLocalDateTime().toString());
      return this;
    }

    public SimpleFilter build() {
      return new SimpleFilter(this);
    }
  }

  public List<String> getQueryMap() {
    return queryMap;
  }
}
