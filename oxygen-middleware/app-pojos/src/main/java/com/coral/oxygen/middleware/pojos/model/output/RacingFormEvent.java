package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import java.io.Serializable;

public class RacingFormEvent implements Serializable {

  private String distance;
  private String going;
  private String raceClass;

  @ChangeDetect
  public String getRaceClass() {
    return raceClass;
  }

  public void setRaceClass(String raceClass) {
    this.raceClass = raceClass;
  }

  public void setDistance(String distance) {
    this.distance = distance;
  }

  @ChangeDetect
  public String getDistance() {
    return distance;
  }

  public void setGoing(String going) {
    this.going = going;
  }

  @ChangeDetect
  public String getGoing() {
    return going;
  }
}
