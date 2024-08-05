package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionSubTab implements Serializable {
  private String name;
  private String uri;
  private String path;
  private boolean enabled;

  public CompetitionSubTab setPathFromParent(CompetitionTab parentCompetitionTab) {
    setPath(parentCompetitionTab.getPath() + getUri());
    return this;
  }

  public CompetitionSubTab setPathFromExistingEntity(CompetitionSubTab existingEntity) {
    setPath(existingEntity.getPath().replace(existingEntity.getUri(), getUri()));
    return this;
  }
}
