package com.ladbrokescoral.oxygen.seo.util;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import org.springframework.stereotype.Component;

@Component
public class QueryFilterBuilder {

  private QueryFilterBuilder() {}

  public static SimpleFilter getClassWithOpenEventsSimpleFilter(String classIds) {
    SimpleFilter.SimpleFilterBuilder builder = createActiveByCategorySimpleFilter(classIds);
    builder.addField(Clazz.HAS_OPEN_EVENT);
    return (SimpleFilter) builder.build();
  }

  static SimpleFilter.SimpleFilterBuilder createActiveByCategorySimpleFilter(String classIds) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField(Clazz.IS_ACTIVE);
    builder.addBinaryOperation(Clazz.CATEGORY_ID, BinaryOperation.equals, classIds);
    builder.addBinaryOperation(Clazz.SITE_CHANNELS, BinaryOperation.contains, "M");
    return builder;
  }

  public static SimpleFilter getClassToSubTypeSimpleFilter() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField(Type.TYPE_HAS_OPEN_EVENT);
    return (SimpleFilter) builder.build();
  }

  public static SimpleFilter getLotteryToSimpleFilter() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addField("lottery.hasOpenDraw");
    return (SimpleFilter) builder.build();
  }

  private static class Clazz {
    static final String CATEGORY_ID = "class.categoryId";
    static final String IS_ACTIVE = "class.isActive";
    static final String HAS_OPEN_EVENT = "class.hasOpenEvent";
    static final String SITE_CHANNELS = "class.siteChannels";
  }

  private static class Type {
    static final String TYPE_HAS_OPEN_EVENT = "type.hasOpenEvent:isTrue";
  }
}
