package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.AbstractModuleData;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class QuickLinkModule extends AbstractFeaturedModule<AbstractModuleData> {

  private String type = "QuickLinkModule";

  @Override
  public ModuleType getModuleType() {
    return ModuleType.QUICK_LINK;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor, String segment) {
    visitor.visit(this, segment);
  }

  public QuickLinkModule copyWithEmptySegmentedData(double segmentOrder) {
    QuickLinkModule result = (QuickLinkModule) copyWithEmptyData();
    result.setModuleSegmentView(null);
    result.setSegments(null);
    result.setSegmentOrder(segmentOrder);
    return result;
  }
}
