package com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.entity;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.domain.Persistable;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "dataRetentionJobs")
@Data
@NoArgsConstructor
@Builder
@AllArgsConstructor
public class DataRetentionJobs implements Persistable<String> {

  @Id
  @JsonView(Views.GetAll.class)
  @EqualsAndHashCode.Include
  private String id;

  private String jobName;
  private String runSatus;
  private Instant startTimestamp;
  private Instant endTimestamp;

  @Override
  public boolean isNew() {
    return false;
  }
}
