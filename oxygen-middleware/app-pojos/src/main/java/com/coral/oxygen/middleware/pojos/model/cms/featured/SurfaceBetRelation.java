package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.Objects;
import lombok.Data;

@Data
public class SurfaceBetRelation {
  private String relationType;
  private String refId;
  private boolean enabled;

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    SurfaceBetRelation that = (SurfaceBetRelation) o;
    return Objects.equals(relationType, that.relationType) && Objects.equals(refId, that.refId);
  }

  @Override
  public int hashCode() {
    return Objects.hash(relationType, refId);
  }
}
