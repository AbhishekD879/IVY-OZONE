package com.egalacoral.spark.timeform.model;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.HashSet;
import java.util.Set;

public class OBRelatedEntity extends Identity implements Serializable {

  @SerializedName(value = "openbet_ids")
  private Set<Integer> obIds;

  /**
   * Gets set of ids of relevant openbet entities
   *
   * @return an Set<Integer> with idf of relevant openbet entities or null if any openbet entities
   *     are not matched with this entity
   */
  public Set<Integer> getOpenBetIds() {
    if (obIds == null) {
      obIds = new HashSet<>();
    }
    return obIds;
  }

  public void setOpenBetIds(Set<Integer> obIds) {
    this.obIds = obIds;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("OBRelatedEntity{");
    sb.append("obIds=").append(obIds);
    sb.append(", ").append(super.toString());
    sb.append('}');
    return sb.toString();
  }
}
