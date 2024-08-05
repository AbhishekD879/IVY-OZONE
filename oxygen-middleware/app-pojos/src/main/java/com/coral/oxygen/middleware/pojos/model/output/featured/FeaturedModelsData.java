package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;

@Getter
@ToString
@EqualsAndHashCode
public class FeaturedModelsData {

  private final List<FeaturedModel> featuredModels;
  private final List<String> sportPages;

  public FeaturedModelsData() {
    this.featuredModels = Collections.emptyList();
    this.sportPages = Collections.emptyList();
  }

  public FeaturedModelsData(List<FeaturedModel> featuredModels, List<SportPage> sportPages) {
    this.featuredModels = featuredModels;
    this.sportPages = sportPages.stream().map(SportPage::getSportId).collect(Collectors.toList());
  }
}
