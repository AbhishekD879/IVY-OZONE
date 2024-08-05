package com.ladbrokescoral.aggregation.model;

import lombok.Builder;
import lombok.Data;
import org.springframework.web.util.UriComponentsBuilder;

@Data
@Builder
public class SilkUrl {

  private String silkId;
  private String endpoint;

  public static class SilkUrlBuilder {
    public SilkUrlBuilder endpoint(String provider, String id, String extension) {
      this.endpoint =
          UriComponentsBuilder.fromHttpUrl(provider).path(id + "." + extension).build().toString();
      return this;
    }

    public SilkUrlBuilder endpoint(String endpoint) {
      this.endpoint = endpoint;
      return this;
    }
  }
}
