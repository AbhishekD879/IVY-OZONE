package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.bigcompetition.dto.AbstractEntity;
import com.ladbrokescoral.oxygen.bigcompetition.dto.ViewType;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModuleType;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public abstract class CompetitionModuleDto extends AbstractEntity {
  private String name;
  private CompetitionModuleType type;
  private int maxDisplay;
  private ViewType viewType;

  @JsonIgnore private String path;

  /**
   * Cut 'competitionUri' substring from /competitionUri/tabUri/subTabUri/moduleId string.
   *
   * @return competitionUri
   */
  @JsonIgnore
  public String getCompetitionUriFromPath() {
    return path != null ? path.split("/")[1] : null;
  }
}
