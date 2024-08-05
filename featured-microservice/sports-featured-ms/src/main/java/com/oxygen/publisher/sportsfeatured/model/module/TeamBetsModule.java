package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.TeamBetsConfig;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class TeamBetsModule extends AbstractFeaturedModule<TeamBetsConfig> {

  private String type = "TeamBetsModule";

  @Override
  public ModuleType getModuleType() {
    return ModuleType.BETS_BASED_ON_YOUR_TEAM;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor, String segment) {
    visitor.visit(this, segment);
  }

  public TeamBetsModule copyWithEmptySegmentedData(double segmentOrder) {
    TeamBetsModule result = (TeamBetsModule) copyWithEmptyData();
    result.setFanzoneModuleSegmentView(null);
    result.setModuleSegmentView(null);
    result.setSegments(null);
    result.setSegmentOrder(segmentOrder);
    result.setFanzoneSegments(null);
    return result;
  }
}
