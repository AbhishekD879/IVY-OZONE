package com.egalacoral.spark.siteserver.model;

import com.google.gson.annotations.SerializedName;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class SSResponse {
  @SerializedName("SSResponse")
  private SSChildResponse response;

  private class SSChildResponse {
    private List<Children> children;

    public List<Children> getChildren() {
      if (children == null) children = new ArrayList<>();
      return children;
    }
  }

  public List<Children> getChildren() {
    return this.response.getChildren();
  }

  private List<Event> getEvents() {
    return this.getChildren().stream()
        .map(s -> s.getEvent())
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  private List<Category> getCategories() {
    return this.getChildren().stream()
        .map(s -> s.getCategory())
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  private Optional<ResponseFooter> getResponseFooter() {
    return this.getChildren().stream()
        .map(s -> s.getResponseFooter())
        .filter(Objects::nonNull)
        .findFirst();
  }
}
