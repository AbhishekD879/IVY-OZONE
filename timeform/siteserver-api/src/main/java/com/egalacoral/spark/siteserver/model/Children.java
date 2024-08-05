package com.egalacoral.spark.siteserver.model;

import com.google.gson.annotations.SerializedName;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Children {
  private Error error;
  private Event event;
  protected Market market;
  protected Outcome outcome;
  private Price price;

  @SerializedName("class")
  private Category category;

  @SerializedName("type")
  protected Type type;

  private ResponseFooter responseFooter;

  public Error getError() {
    return error;
  }

  public Event getEvent() {
    return event;
  }

  public Market getMarket() {
    return market;
  }

  public Outcome getOutcome() {
    return outcome;
  }

  public Price getPrice() {
    return price;
  }

  public Category getCategory() {
    return category;
  }

  public Type getType() {
    return type;
  }

  public ResponseFooter getResponseFooter() {
    return responseFooter;
  }

  @Override
  public String toString() {
    return "{"
        + "error="
        + error
        + ", event="
        + event
        + ", market="
        + market
        + ", outcome="
        + outcome
        + ", price="
        + price
        + ", category="
        + category
        + ", type="
        + type
        + ", responseFooter="
        + responseFooter
        + '}';
  }
}
