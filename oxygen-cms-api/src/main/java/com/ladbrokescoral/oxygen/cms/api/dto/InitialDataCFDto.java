package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;
import lombok.Data;

@Data
@JsonIgnoreProperties(
    value = {"footerMenu", "navigationPoints", "modularContent", "sportCategories"})
public class InitialDataCFDto extends InitialDataDto {
  private List<FooterMenuSegmentedDto> footerMenuCollection;
  private List<NavigationPointSegmentedDto> navigationPointsCollection;
  private ModularSegmentedContentDto modularContentCollection;
  private List<BaseModularContentDto> modularContentUniversal;
  private List<InitialDataSportCategorySegmentedDto> sportCategoryCollection;
  private List<String> segmentCollection;
}
