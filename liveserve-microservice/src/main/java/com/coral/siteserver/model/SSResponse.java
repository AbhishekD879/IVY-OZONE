package com.coral.siteserver.model;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class SSResponse implements Serializable {

  private static final long serialVersionUID = -7971917325815615715L;

  @SerializedName("SSResponse")
  protected SSChildResponse response = new SSChildResponse();

  public static class SSChildResponse implements Serializable {

    private static final long serialVersionUID = -2745982663670441896L;

    private List<Children> children;

    public List<Children> getChildren() {
      if (children == null) children = new ArrayList<>();
      return children;
    }
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
