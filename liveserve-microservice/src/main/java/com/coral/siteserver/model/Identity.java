package com.coral.siteserver.model;

import java.io.Serializable;
import java.util.Objects;
import java.util.UUID;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public abstract class Identity implements Serializable {

  private static final long serialVersionUID = 3103745239880735522L;

  private final String uuid;

  public Identity() {
    this.uuid = UUID.randomUUID().toString();
  }

  public String getUUID() {
    return uuid;
  }

  @Override
  public String toString() {
    return this.getClass().getSimpleName() + ": " + this.uuid + " ";
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Identity identity = (Identity) o;
    return Objects.equals(identity.uuid, this.uuid);
  }

  @Override
  public int hashCode() {
    return Objects.hash(this.uuid);
  }
}
