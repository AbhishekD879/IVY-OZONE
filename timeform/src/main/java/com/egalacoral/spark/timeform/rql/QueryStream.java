package com.egalacoral.spark.timeform.rql;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import net.jazdw.rql.converter.Converter;
import net.jazdw.rql.parser.ASTNode;
import net.jazdw.rql.parser.RQLParser;
import net.jazdw.rql.parser.RQLParserException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class QueryStream<T> {

  private static final Logger LOGGER = LoggerFactory.getLogger(QueryStream.class);

  private List<T> data;
  private QueryStream<T> instance;
  private RQLParser parser = new RQLParser();
  private ListObjectFilter<T> listFilter = new ListObjectFilter<>();

  public QueryStream(List<T> data) {
    this.data = data;
    this.instance = this;
    Converter.CONVERTERS.put("date", Converters.DATE);
    parser = new RQLParser(new Converter(new AutoValueConverter()));
  }

  public static <T> QueryStream<T> of(List<T> elements, String filter) {
    QueryStream<T> queryStream = new QueryStream<T>(elements);
    return queryStream.filter(filter);
  }

  public QueryStream<T> filter(String filter) {
    if (filter != null) {
      filter = filter.trim();
      try {
        LOGGER.info("Going to filter by {}", filter);
        ASTNode node = parser.parse(filter);
        data = node.accept(listFilter, data);
      } catch (NullPointerException | IllegalArgumentException e) {
        LOGGER.info("Invalid filter {}", e);
        throwInvalidFilterFormatException(filter);
      }
    }
    return instance;
  }

  protected void throwInvalidFilterFormatException(String filter) {
    throw new UnsupportedOperationException(
        String.format(
            "Invalid filter format : '%s'. Valid format : (fieldName1>value1|fieldName2=value2)&field3<=value3",
            filter));
  }

  public Stream<T> stream() {
    return data.stream();
  }

  private void limit(Integer count, Integer start) {
    if (start != null) {
      data = data.stream().skip(start).collect(Collectors.toList());
    }

    if (count != null) {
      data = data.stream().limit(count).collect(Collectors.toList());
    }
  }

  /**
   * Sort in format : "-fieldName1,-fieldName2"
   *
   * @param sort
   */
  public void sort(String sort) {
    if (sort != null) {
      try {
        LOGGER.info("Going to sort by {}", sort);
        ASTNode node = parser.parse("sort(" + sort + ")");
        data = node.accept(listFilter, data);
      } catch (RQLParserException e) {
        throw new UnsupportedOperationException(
            String.format(
                "Invalid sort format  '%s'. Valid format : +fieldName1,-fieldName2", sort),
            e);
      }
    }
  }

  public List<T> toList() {
    return stream().collect(Collectors.toList());
  }

  public static <T> QueryStream<T> of(List<T> elements, String filter, String orderby) {
    QueryStream<T> stream = of(elements, filter);
    stream.sort(orderby);
    return stream;
  }

  public static <T> QueryStream<T> of(
      List<T> elements, String filter, String orderby, Integer count, Integer start) {
    QueryStream<T> stream = of(elements, filter, orderby);
    stream.limit(count, start);
    return stream;
  }
}
