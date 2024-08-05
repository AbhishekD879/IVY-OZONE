package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.fasterxml.jackson.annotation.JsonFilter;

@JsonFilter("cloudFlareFeatureModel")
public class CloudFlareFeatureModel extends FeaturedModel {

  public CloudFlareFeatureModel(FeaturedModel model) {
    super(
        model.getPageId(),
        model.getDirectiveName(),
        model.getEventsModuleData(),
        model.getModules(),
        model.getShowTabOn(),
        model.getTitle(),
        model.isVisible(),
        model.isFeatureStructureChanged(),
        model.getSegmentWiseModules(),
        model.getFanzoneSegmentWiseModules(),
        model.getSurfaceBetModule(),
        model.getQuickLinkModule(),
        model.getInplayModule(),
        model.getTeamBetsModule(),
        model.getFanBetsModule(),
        model.isSegmented(),
        model.isUseFSCCached());
  }
}
