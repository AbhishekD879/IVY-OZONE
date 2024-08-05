package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class InplayModule extends AbstractFeaturedModule<SportSegment> {

  private Integer totalEvents;

  private int maxEventCount;

  private Map<String, SegmentView> moduleSegmentView = new HashMap<>();

  public InplayModule() {
    this.showExpanded = true;
  }

  @JsonIgnore
  @Override
  public ModuleType getModuleType() {
    return ModuleType.INPLAY;
  }

  @Override
  public String toString() {
    return super.toString();
  }

  public InplayModule copyWithEmptySegmentedData(double segmentOrder) {
    InplayModule result = (InplayModule) copyWithEmptyData();
    result.setModuleSegmentView(null);
    result.setSegments(null);
    result.setSegmentOrder(segmentOrder);
    return result;
  }
}
