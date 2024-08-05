package com.egalacoral.spark.timeform.rql;

import java.lang.reflect.InvocationTargetException;
import java.util.*;
import java.util.regex.Pattern;
import net.jazdw.rql.converter.Converter;
import net.jazdw.rql.converter.ConverterException;
import net.jazdw.rql.parser.ASTNode;
import net.jazdw.rql.parser.ASTVisitor;
import org.apache.commons.beanutils.BeanComparator;
import org.apache.commons.beanutils.ConvertUtils;
import org.apache.commons.beanutils.PropertyUtils;
import org.apache.commons.collections.comparators.ComparatorChain;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ListObjectFilter<T> implements ASTVisitor<List<T>, List<T>> {

  private static final Logger LOGGER = LoggerFactory.getLogger(ListObjectFilter.class);
  private static final String SUPPORTED_OPERATORS =
      "match(fieldname,value) , > , >= , < , <= , = , & , | ";

  /*
   * (non-Javadoc)
   *
   * @see net.jazdw.rql.parser.ASTVisitor#visit(net.jazdw.rql.parser.ASTNode, java.lang.Object)
   */
  @Override
  public List<T> visit(ASTNode node, List<T> list) {
    LOGGER.info("Going to handle node {}", node);
    switch (node.getName()) {
      case "and":
        list = handleAnd(node, list);
        return list;
      case "or":
        Set<T> set = handleOr(node, list);
        return new ArrayList<>(set);
      case "eq":
      case "gt":
      case "ge":
      case "lt":
      case "le":
      case "ne":
        return handleCompare(node, list);
      case "like":
      case "match":
        return handleMatch(node, list);
      case "limit":
        return handleLimit(node, list);
      case "sort":
        return handleSort(node, list);
      default:
        throw new UnsupportedOperationException(
            String.format(
                "Encountered unknown operator '%s'. Supported operators :%s ",
                node.getName(), SUPPORTED_OPERATORS));
    }
  }

  protected List<T> handleSort(ASTNode node, List<T> list) {
    Object object;
    if (list.isEmpty()) {
      return list;
    } else {
      object = list.get(0);
    }
    ComparatorChain cc = new ComparatorChain();
    for (Object obj : node) {
      String sortOption = (String) obj;
      boolean desc = sortOption.startsWith("-");
      boolean asc = sortOption.startsWith("+");
      if (!desc && !asc) {
        throw new UnsupportedOperationException(
            String.format(
                "Invalid sort format  '%s'. Valid format : +fieldName1,-fieldName2", sortOption));
      }
      String propertyName = sortOption.substring(1);
      getProperty(object, propertyName);
      cc.addComparator(new BeanComparator<T>(propertyName), desc);
    }
    // copy the list as we are modifying it
    list = new ArrayList<>(list);
    Collections.sort(list, cc);
    return list;
  }

  protected List<T> handleLimit(ASTNode node, List<T> list) {
    int limit = (int) node.getArgument(0);
    int offset = node.getArgumentsSize() > 1 ? (int) node.getArgument(1) : 0;

    if (offset > list.size() - 1) {
      return Collections.emptyList();
    }

    int toIndex = offset + limit;
    if (toIndex > list.size()) {
      toIndex = list.size();
    }

    return list.subList(offset, toIndex);
  }

  protected List<T> handleMatch(ASTNode node, List<T> list) {
    String propName;
    List<T> result;
    propName = (String) node.getArgument(0);
    String matchString = node.getArgument(1).toString();
    Pattern matchPattern =
        Pattern.compile(
            matchString.replace("*", ".*"), Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE);
    LOGGER.info("Match '{}' with '{}'", propName, matchPattern);

    result = new ArrayList<>();

    for (T item : list) {
      Object property = getProperty(item, propName);

      String stringProperty;
      if (property instanceof String) {
        stringProperty = (String) property;
      } else {
        try {
          stringProperty = (String) ConvertUtils.convert(property, String.class);
        } catch (RuntimeException e) {
          throw new UnsupportedOperationException(
              String.format("Property '%s' is not a string", propName), e);
        }
      }

      if (matchPattern.matcher(stringProperty).matches()) {
        result.add(item);
      }
    }
    return result;
  }

  protected List<T> handleCompare(ASTNode node, List<T> list) {
    String propName = (String) node.getArgument(0);
    Object test = node.getArgumentsSize() > 1 ? node.getArgument(1) : null;
    List<T> result = new ArrayList<>();

    for (T item : list) {
      Object property = getProperty(item, propName);

      if (property == null) {
        continue;
      }

      Comparable<Object> comparableProperty;
      if (property instanceof Comparable) {
        comparableProperty = (Comparable<Object>) property;
      } else {
        throw new UnsupportedOperationException(
            String.format("Property '%s' is not comparable", propName));
      }

      int comparisonValue;
      try {
        comparisonValue = comparableProperty.compareTo(test);
      } catch (ClassCastException e) {
        try {
          if (property instanceof Date) {
            test = convertDate(test, propName);
          } else {
            test = ConvertUtils.convert(test, comparableProperty.getClass());
          }
          comparisonValue = comparableProperty.compareTo(test);
        } catch (ClassCastException castException) {
          throw new UnsupportedOperationException(
              String.format(
                  "Couldn't compare '%s' to '%s'",
                  property.toString(), test != null ? test.toString() : ""));
        }
      }

      if (checkComparisonValue(node.getName(), comparisonValue)) {
        result.add(item);
      }
    }
    return result;
  }

  protected Object convertDate(Object test, String propName) {
    if (test instanceof DateTime) {
      test = ((DateTime) test).toDate();
    } else {
      try {
        test = ((DateTime) Converter.DATE.convert(test.toString())).toDate();
      } catch (ConverterException e) {
        throw new UnsupportedOperationException(
            String.format("Invalid data format for property '%s' = '%s'", propName, test), e);
      }
    }
    return test;
  }

  protected Set<T> handleOr(ASTNode node, List<T> list) {
    Set<T> set = new LinkedHashSet<>();
    for (Object obj : node) {
      if (obj instanceof ASTNode) {
        set.addAll(((ASTNode) obj).accept(this, list));
      } else {
        throw new UnsupportedOperationException(
            "Encountered a non-ASTNode argument in OR statement");
      }
    }
    return set;
  }

  protected List<T> handleAnd(ASTNode node, List<T> list) {
    for (Object obj : node) {
      if (obj instanceof ASTNode) {
        list = ((ASTNode) obj).accept(this, list);
      } else {
        throw new UnsupportedOperationException(
            "Encountered a non-ASTNode argument in AND statement");
      }
    }
    return list;
  }

  private boolean checkComparisonValue(String name, int value) {
    switch (name) {
      case "eq":
        return value == 0;
      case "gt":
        return value > 0;
      case "ge":
        return value >= 0;
      case "lt":
        return value < 0;
      case "le":
        return value <= 0;
      case "ne":
        return value != 0;
    }
    return false;
  }

  private Object getProperty(Object item, String propName) {
    Object property;
    try {
      property = PropertyUtils.getProperty(item, propName);
    } catch (IllegalAccessException | InvocationTargetException | NoSuchMethodException e) {
      throw new UnsupportedOperationException(
          String.format(
              "Could not find property '%s' in object '%s'", propName, item.getClass().getName()));
    }
    return property;
  }
}
