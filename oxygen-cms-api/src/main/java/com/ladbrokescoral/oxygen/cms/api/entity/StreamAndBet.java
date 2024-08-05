package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "streamAndBet")
@Data
@EqualsAndHashCode(callSuper = true)
public class StreamAndBet extends AbstractEntity implements HasBrand {

  @NotBlank private String brand;
  private List<SABChildElement> children;

  // StreamAndBet Child Element, basically a Node in categories tree
  @Data
  @NoArgsConstructor
  public static class SABChildElement {

    private Integer siteServeId;
    private String name;
    private String showItemFor;
    private String selection;
    private List<SABChildElement> children;
  }
}
