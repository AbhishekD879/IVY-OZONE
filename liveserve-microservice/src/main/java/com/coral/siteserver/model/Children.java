package com.coral.siteserver.model;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.Map;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Children implements Serializable {

  private static final long serialVersionUID = -8003336285319024860L;

  private Error error;
  private Event event;
  protected Market market;
  protected Outcome outcome;
  private Price price;

  @SerializedName("class")
  private Category category;

  @SerializedName("type")
  protected Type type;

  @SerializedName("aggregation")
  protected Aggregation aggregation;

  protected RacingFormOutcome racingFormOutcome;
  private ResponseFooter responseFooter;
  protected Map eventPeriod;
  protected Map eventParticipant;

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

  public Aggregation getAggregation() {
    return aggregation;
  }

  public ResponseFooter getResponseFooter() {
    return responseFooter;
  }

  public Map<String, Object> getEventPeriod() {
    return eventPeriod;
  }

  public Map<String, Object> getEventParticipant() {
    return eventParticipant;
  }

  public RacingFormOutcome getRacingFormOutcome() {
    return racingFormOutcome;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Children{");
    sb.append("error=").append(error);
    sb.append(", event=").append(event);
    sb.append(", market=").append(market);
    sb.append(", outcome=").append(outcome);
    sb.append(", price=").append(price);
    sb.append(", category=").append(category);
    sb.append(", type=").append(type);
    sb.append(", aggregation=").append(aggregation);
    sb.append(", racingFormOutcome=").append(racingFormOutcome);
    sb.append(", responseFooter=").append(responseFooter);
    sb.append(", eventPeriod=").append(eventPeriod);
    sb.append(", eventParticipant=").append(eventParticipant);
    sb.append('}');
    return sb.toString();
  }
}
