package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class InplayModule extends AbstractFeaturedModule<SportSegment> {

  private String type = "InplayModule";

  private Integer totalEvents;

  @Override
  public ModuleType getModuleType() {
    return ModuleType.IN_PLAY;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor, String segment) {
    visitor.visit(this, segment);
  }

  public InplayModule copyWithEmptySegmentedData(double segmentOrder) {
    InplayModule result = (InplayModule) copyWithEmptyData();
    result.setModuleSegmentView(null);
    result.setSegments(null);
    result.setSegmentOrder(segmentOrder);
    return result;
  }

  @Override
  public String toString() {
    return super.toString();
  }
}
