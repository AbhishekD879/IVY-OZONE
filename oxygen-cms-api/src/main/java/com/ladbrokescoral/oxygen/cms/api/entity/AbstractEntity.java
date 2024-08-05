package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedBy;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.annotation.Transient;
import org.springframework.data.domain.Persistable;

@Data
@SuperBuilder
@NoArgsConstructor
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public abstract class AbstractEntity implements Persistable<String> {

  @Id
  @JsonView(Views.GetAll.class)
  @EqualsAndHashCode.Include
  private String id;

  /**
   * FIXME: should be done in this way or remove at all.
   * No need for createdByUserName and updatedByUserName.
   * <pre>
   * @CreatedBy private UserDetails createdBy;
   * @LastModifiedBy private UserDetails updatedBy;
   * <pre>
   */
  @CreatedBy private String createdBy;

  @Transient private String createdByUserName;
  @LastModifiedBy private String updatedBy;
  @Transient private String updatedByUserName;

  @CreatedDate
  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant createdAt;

  @LastModifiedDate
  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant updatedAt;

  @Override
  @JsonIgnore
  public boolean isNew() {
    return null == id;
  }
}
