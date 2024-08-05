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
public class CompetitionTab extends AbstractEntity {
  @NotEmpty private String name;
  @NotEmpty private String uri;
  private String path;
  private boolean hasSubtabs;
  private boolean enabled;
  @DBRef private List<CompetitionSubTab> competitionSubTabs = new ArrayList<>();
  @DBRef private List<CompetitionModule> competitionModules = new ArrayList<>();

  public CompetitionTab setPathFromParent(Competition parentCompetition) {
    setPath(parentCompetition.getPath() + getUri());
    return this;
  }

  public CompetitionTab setPathFromExistingEntity(CompetitionTab existingEntity) {
    setPath(existingEntity.getPath().replace(existingEntity.getUri(), getUri()));
    return this;
  }
}
