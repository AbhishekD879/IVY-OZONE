package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "brands")
@Data
@EqualsAndHashCode(callSuper = true)
public class Brand extends SortableEntity {

  public static final String BMA = "bma";
  public static final String LADBROKES = "ladbrokes";

  // FIXME: should be enum OR removed at all. use DB.
  public static final List<String> BRAND_LIST =
      Collections.unmodifiableList(
          Arrays.asList(
              "rcomb", BMA, "secondscreen", "gf", "partner", "retail", "connect", LADBROKES));

  @Indexed(unique = true)
  @NotBlank
  private String brandCode;

  private Boolean disabled = false;
  private String key;
  @NotBlank private String title;
  private String siteServerEndPoint;
  private String spotlightEndpoint;
  private String spotlightApiKey;
  private String dataFabricEndPoint;
  private String dataFabricApiKey;
}
