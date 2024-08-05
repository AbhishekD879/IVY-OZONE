package com.egalacoral.spark.siteserver.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class ReferenceEachWayTerms extends IdentityWithChildren {
  private String id;
  private Integer places;
}
