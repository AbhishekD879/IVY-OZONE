package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import java.util.Set;
import lombok.*;

@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@Data
public class AemBannersImg extends AbstractModuleData {

  @SerializedName("@type")
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

  @Builder
  public AemBannersImg(
      String guid,
      PageType pageType,
      String offerTitle,
      String offerName,
      String imgUrl,
      String webUrl,
      String roxanneWebUrl,
      String appUrl,
      String roxanneAppUrl,
      String webTarget,
      String appTarget,
      String selectionId,
      String altText,
      String webTandC,
      String webTandCLink,
      String mobTandCLink,
      String isScrbrd,
      String scrbrdEventId,
      String scrbrdPosition,
      String scrbrdTypeId,
      int displayOrder,
      Set<String> imsLevel,
      Set<String> userType,
      Set<String> selectChannels) {
    super(guid, pageType);
    this.offerTitle = offerTitle;
    this.offerName = offerName;
    this.imgUrl = imgUrl;
    this.webUrl = webUrl;
    this.roxanneWebUrl = roxanneWebUrl;
    this.appUrl = appUrl;
    this.roxanneAppUrl = roxanneAppUrl;
    this.webTarget = webTarget;
    this.appTarget = appTarget;
    this.selectionId = selectionId;
    this.altText = altText;
    this.webTandC = webTandC;
    this.webTandCLink = webTandCLink;
    this.mobTandCLink = mobTandCLink;
    this.isScrbrd = isScrbrd;
    this.scrbrdEventId = scrbrdEventId;
    this.scrbrdPosition = scrbrdPosition;
    this.scrbrdTypeId = scrbrdTypeId;
    this.displayOrder = displayOrder;
    this.imsLevel = imsLevel;
    this.userType = userType;
    this.selectChannels = selectChannels;
  }

  @ChangeDetect
  public String getType() {
    return type;
  }

  @ChangeDetect
  public String getOfferTitle() {
    return offerTitle;
  }

  @ChangeDetect
  public String getOfferName() {
    return offerName;
  }

  @ChangeDetect
  public String getWebUrl() {
    return webUrl;
  }

  @ChangeDetect
  public String getRoxanneWebUrl() {
    return roxanneWebUrl;
  }

  @ChangeDetect
  public String getAppUrl() {
    return appUrl;
  }

  @ChangeDetect
  public String getRoxanneAppUrl() {
    return roxanneAppUrl;
  }

  @ChangeDetect
  public String getWebTarget() {
    return webTarget;
  }

  @ChangeDetect
  public String getAppTarget() {
    return appTarget;
  }

  @ChangeDetect
  public String getSelectionId() {
    return selectionId;
  }

  @ChangeDetect
  public String getAltText() {
    return altText;
  }

  @ChangeDetect
  public String getWebTandC() {
    return webTandC;
  }

  @ChangeDetect
  public String getWebTandCLink() {
    return webTandCLink;
  }

  @ChangeDetect
  public String getMobTandCLink() {
    return mobTandCLink;
  }

  @ChangeDetect
  public String getIsScrbrd() {
    return isScrbrd;
  }

  @ChangeDetect
  public String getScrbrdEventId() {
    return scrbrdEventId;
  }

  @ChangeDetect
  public String getScrbrdPosition() {
    return scrbrdPosition;
  }

  @ChangeDetect
  public String getScrbrdTypeId() {
    return scrbrdTypeId;
  }

  @ChangeDetect
  public int getDisplayOrder() {
    return displayOrder;
  }

  @ChangeDetect
  public String getImgUrl() {
    return imgUrl;
  }

  @ChangeDetect
  public Set<String> getImsLevel() {
    return imsLevel;
  }

  @ChangeDetect
  public Set<String> getUserType() {
    return userType;
  }

  @ChangeDetect
  public Set<String> getSelectChannels() {
    return selectChannels;
  }
}
