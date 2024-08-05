package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.siteserver.model.*;
import com.egalacoral.spark.timeform.model.greyhound.Entry;
import java.util.Arrays;
import java.util.stream.Collectors;

public class SiteServerDataWrappers {

  public static class TypeForTest extends Type {

    public TypeForTest(int id, String name) {
      this.id = id;
      this.name = name;
    }
  }

  public static class EventForTest extends Event {

    public EventForTest(String id, String name, int typeId, Market... markets) {
      this.id = id;
      this.name = name;
      this.typeId = String.valueOf(typeId);
      this.drilldownTagNames = name;

      this.children =
          Arrays.stream(markets).map(m -> new ChildrenForTest(m)).collect(Collectors.toList());
    }
  }

  public static class ChildrenForTest extends Children {

    public ChildrenForTest(Market market) {
      this.market = market;
    }

    public ChildrenForTest(Outcome outcome) {
      this.outcome = outcome;
    }
  }

  public static class MarketForTest extends Market {
    public MarketForTest(String id, String name, Outcome... outcomes) {
      this.id = id;
      this.name = name;
      this.children =
          Arrays.stream(outcomes).map(o -> new ChildrenForTest(o)).collect(Collectors.toList());
    }
  }

  public static class OutcomeForTest extends Outcome {
    public OutcomeForTest(String id, String name) {
      this.id = id;
      this.name = name;
    }
  }

  public static class EntryForTest extends Entry {

    @Override
    public String getStatusDescription() {
      return "status1";
    }
  }
}
