package com.egalacoral.spark.siteserver.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.Data;

public class SSResponse {

  @JsonProperty("SSResponse")
  public SSChildResponse response;

  // FIXME: need rework. we have #IdentityWithChildren or vice-versa
  @Data
  private static class SSChildResponse {
    private List<Children> children = new ArrayList<>();
  }

  public List<Children> getChildren() {
    List<Children> children = this.response.getChildren();
    Optional<ResponseFooter> responseFooterOptional = this.getResponseFooter();
    if (responseFooterOptional.isPresent()) {
      ResponseFooter responseFooter = responseFooterOptional.get();
      String creationTime = responseFooter.getCreationTime();
      for (Children ch : children) {
        Event event = ch.getEvent();
        if (event != null) {
          if (event.getResponseCreationTime() != null) {
            break;
          } else {
            event.setResponseCreationTime(creationTime);
          }
        }
      }
    }
    return children;
  }

  private Optional<ResponseFooter> getResponseFooter() {
    return this.response.getChildren().stream()
        .map(Children::getResponseFooter)
        .filter(Objects::nonNull)
        .findFirst();
  }
}
