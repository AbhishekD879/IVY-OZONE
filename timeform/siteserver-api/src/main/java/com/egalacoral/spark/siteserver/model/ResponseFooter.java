package com.egalacoral.spark.siteserver.model;

import org.joda.time.DateTime;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class ResponseFooter {
  protected Double cost;
  protected DateTime creationTime;
  protected String liveServLastMsgId;

  public Double getCost() {
    return cost;
  }

  public DateTime getCreationTime() {
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
