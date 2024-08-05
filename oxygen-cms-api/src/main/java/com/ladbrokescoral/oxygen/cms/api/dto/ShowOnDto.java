package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.ArrayList;
import java.util.List;

public class ShowOnDto {

  @JsonProperty("routes")
  private String routes = null;

  @JsonProperty("sports")
  private List<String> sports = null;

  public ShowOnDto routes(String routes) {
    this.routes = routes;
    return this;
  }

  /**
   * Get routes
   *
   * @return routes
   */
  public String getRoutes() {
    return routes;
  }

  public void setRoutes(String routes) {
    this.routes = routes;
  }

  public ShowOnDto addSportsItem(String sport) {
    if (this.sports == null) {
      this.sports = new ArrayList<>();
    }
    this.sports.add(sport);
    return this;
  }

  public ShowOnDto sports(List<String> sports) {
    this.sports = sports;
    return this;
  }

  /**
   * Get sports
   *
   * @return sports
   */
  public List<String> getSports() {
    return sports;
  }

  public void setSports(List<String> sports) {
    this.sports = sports;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    ShowOnDto showOnDto = (ShowOnDto) o;

    if (routes != null ? !routes.equals(showOnDto.routes) : showOnDto.routes != null) return false;
    return sports != null ? sports.equals(showOnDto.sports) : showOnDto.sports == null;
  }

  @Override
  public int hashCode() {
    int result = routes != null ? routes.hashCode() : 0;
    result = 31 * result + (sports != null ? sports.hashCode() : 0);
    return result;
  }
}
