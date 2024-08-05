package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionTab implements Serializable {
  private String name;
  private String uri;
  private String path;
  private boolean hasSubtabs;
  private boolean enabled;
  private List<CompetitionSubTab> competitionSubTabs = new ArrayList<>();

  public CompetitionTab setPathFromParent(Competition parentCompetition) {
    setPath(parentCompetition.getPath() + getUri());
    return this;
  }

  public CompetitionTab setPathFromExistingEntity(CompetitionTab existingEntity) {
    setPath(existingEntity.getPath().replace(existingEntity.getUri(), getUri()));
    return this;
  }
}
