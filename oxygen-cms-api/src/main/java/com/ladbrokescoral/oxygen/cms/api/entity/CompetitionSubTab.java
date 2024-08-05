package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.ArrayList;
import java.util.List;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.DBRef;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionSubTab extends AbstractEntity {
  @NotEmpty private String name;
  @NotEmpty private String uri;
  private String path;
  private boolean enabled;
  @DBRef private List<CompetitionModule> competitionModules = new ArrayList<>();

  public CompetitionSubTab setPathFromParent(CompetitionTab parentCompetitionTab) {
    setPath(parentCompetitionTab.getPath() + getUri());
    return this;
  }

  public CompetitionSubTab setPathFromExistingEntity(CompetitionSubTab existingEntity) {
    setPath(existingEntity.getPath().replace(existingEntity.getUri(), getUri()));
    return this;
  }
}
