package com.oxygen.publisher.sportsfeatured.model.module.data;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Set;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@NoArgsConstructor
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
public class AemBannersImg extends AbstractModuleData {

  @JsonProperty("@type")
  private final String type = "AemBannersImg";

  private String offerTitle;
  private String offerName;
  private String imgUrl;
  private String webUrl;

  // must be removed after Roxanne release go live
  private String roxanneWebUrl;

  private String appUrl;
  // must be removed after Roxanne release go live
  private String roxanneAppUrl;

  private String webTarget;
  private String appTarget;
  private String selectionId;
  private String altText;
  private String webTandC;
  private String webTandCLink;
  private String mobTandCLink;
  private String isScrbrd;
  private String scrbrdEventId;
  private String scrbrdPosition;
  private String scrbrdTypeId;
  private int displayOrder;
  private Set<String> imsLevel;
  private Set<String> userType;
  private Set<String> selectChannels;
}
