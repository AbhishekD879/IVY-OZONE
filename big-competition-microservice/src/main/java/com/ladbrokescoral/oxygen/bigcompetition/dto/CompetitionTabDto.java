package com.ladbrokescoral.oxygen.bigcompetition.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionTabDto extends AbstractEntity {
  private String name;
  private String title;
  private String uri;
  private String path;
  private boolean hasSubtabs;
  private List<CompetitionSubTabDto> competitionSubTabs = new ArrayList<>();
  private List<CompetitionModuleDto> competitionModules = new ArrayList<>();
}
