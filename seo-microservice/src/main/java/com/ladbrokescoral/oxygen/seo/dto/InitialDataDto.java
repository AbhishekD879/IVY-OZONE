package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;

@Data
public class InitialDataDto {

  private List<ModularContentDto> modularContent;

  @JsonInclude(JsonInclude.Include.NON_EMPTY)
  private List<InitialDataSportCategoryDto> sportCategories;
}
