package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

@Data
@NoArgsConstructor
@SuperBuilder
@EqualsAndHashCode(callSuper = true)
public class Relation extends SortableEntity {

  @NotNull private RelationType relatedTo;
  @NotNull private String refId;
  @EqualsAndHashCode.Exclude @NotNull @Builder.Default private boolean enabled = Boolean.TRUE;
}
