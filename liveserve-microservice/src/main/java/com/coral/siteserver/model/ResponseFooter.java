package com.coral.siteserver.model;

import java.io.Serializable;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class ResponseFooter implements Serializable {

  private static final long serialVersionUID = -4960521920137105663L;

  protected Double cost;
  protected String creationTime;
  protected String liveServLastMsgId;

  public Double getCost() {
    return cost;
  }

  public String getCreationTime() {
    return creationTime;
  }

  public String getLiveServLastMsgId() {
    return liveServLastMsgId;
  }

  @Override
  public String toString() {
    return "ResponseFooter{"
        + "cost="
        + cost
        + ", creationTime="
        + creationTime
        + ", liveServLastMsgId='"
        + liveServLastMsgId
        + '\''
        + '}';
  }
}
