package com.egalacoral.spark.timeform.model;

import java.io.Serializable;
import java.util.Date;
import java.util.Objects;
import java.util.UUID;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public abstract class Identity implements Serializable {

  private static final long serialVersionUID = -7961786180626067022L;
  private final String uuid;
  private Date updateDate = new Date();

  public Identity() {
    this.uuid = UUID.randomUUID().toString();
  }

  public String getUUID() {
    return this.uuid;
  }

  public Date getUpdateDate() {
    return updateDate;
  }

  public void setUpdateDate(Date updateDate) {
    this.updateDate = updateDate;
  }

  @Override
  public String toString() {
    return this.getClass().getSimpleName() + ": UUID[" + this.getUUID() + "]";
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Identity identity = (Identity) o;
    return Objects.equals(uuid, identity.getUUID());
  }

  @Override
  public int hashCode() {
    return Objects.hash(this.uuid);
  }
}
