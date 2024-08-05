package com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.entity;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.domain.Persistable;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "jobs")
@Data
@NoArgsConstructor
public class Jobs implements Persistable<String> {

  @Id
  @JsonView(Views.GetAll.class)
  @EqualsAndHashCode.Include
  private String id;

  private String jobName;
  private String jobStatus;
  private Instant insertedDate;
  private Instant updatedDate;

  @Override
  public boolean isNew() {
    return false;
  }
}
