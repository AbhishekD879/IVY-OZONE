package com.egalacoral.spark.siteserver.model;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import java.io.IOException;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class RacingResult extends IdentityWithChildren {

  private String id;
  private String name;
  private String eventStatusCode;
  private Integer displayOrder;
  private String siteChannels;
  private String eventSortCode;
  private String startTime;

  // FIXME: make sure that UI relly need `boolean`
  @JsonDeserialize(using = YNDashDeserializer.class)
  private Boolean rawIsOffCode;

  private Boolean isResulted;
  private String isFinished;
  private String classId;
  private String typeId;
  private String sportId;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private String className;
  private String classDisplayOrder;
  private String classSortCode;
  private String classFlagCodes;
  private String typeName;
  private String typeDisplayOrder;
  private String typeFlagCodes;

  private static class YNDashDeserializer extends JsonDeserializer<Boolean> {

    @Override
    public Boolean deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {

      // FIXME: need investigation regarding correct format and `null` values.
      switch (p.getValueAsString()) {
        case "Y":
          return Boolean.TRUE;
        case "N":
          return Boolean.FALSE;
        case "-":
          return null;
        default:
          return null;
      }
    }
  }
}
