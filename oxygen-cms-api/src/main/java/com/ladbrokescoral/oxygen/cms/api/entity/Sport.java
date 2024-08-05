package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

// Olympic sport
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "sports")
@Data
@EqualsAndHashCode(callSuper = true)
public class Sport extends SortableEntity implements HasBrand {

  private String alt;

  @NotBlank(groups = {ValidationPost.class, ValidationPut.class})
  private String brand;

  @NotNull(groups = {ValidationPost.class, ValidationPut.class})
  private Integer categoryId;

  private String collectionType;
  private boolean disabled;

  @NotBlank(groups = {ValidationPut.class})
  private String dispSortName;

  private Filename filename;
  private Filename svgFilename;
  private Filename icon;
  private Integer heightMedium;
  private Integer heightMediumIcon;
  private Integer heightSmall;
  private Integer heightSmallIcon;

  @NotEmpty(groups = {ValidationPost.class, ValidationPut.class})
  private String imageTitle;

  private Boolean inApp;
  private Boolean isOutrightSport;
  private Boolean isMultiTemplateSport;
  private String lang;
  private String outcomesTemplateType1;
  private String outcomesTemplateType2;
  private String outcomesTemplateType3;

  @NotBlank(groups = {ValidationPut.class})
  private String primaryMarkets;

  private Boolean showInPlay;
  private String spriteClass;
  private String ssCategoryCode;
  private String svg;
  private String svgId;
  private Tab tabCompetitions;
  private Tab tabCoupons;
  private Tab tabJackpot;
  private Tab tabLive;
  private Tab tabMatches;
  private Tab tabOutrights;
  private Tab tabSpecials;
  private String targetUri;

  @NotEmpty(groups = {ValidationPost.class, ValidationPut.class})
  @Pattern(
      regexp = "^([0-9]+,)*[0-9]+$",
      message = "typeIds should be comma-separated numbers",
      groups = {ValidationPost.class, ValidationPut.class})
  private String typeIds;

  private String uriMedium;
  private String uriSmall;
  private String viewByFilters;
  private Integer widthMedium;
  private Integer widthMediumIcon;
  private Integer widthSmall;
  private Integer widthSmallIcon;
  private String defaultTab;
  private Integer heightLarge;
  private Integer heightLargeIcon;
  private String uriLarge;
  private Integer widthLarge;
  private Integer widthLargeIcon;
  private String uriSmallIcon;
  private String uriMediumIcon;
  private String uriLargeIcon;

  public void clearImageFile() {
    setFilename(null);
    setUriSmall(null);
    setUriMedium(null);
    setUriLarge(null);
  }

  public void clearSvg() {
    setSvgFilename(null);
    setSvg(null);
  }

  public void clearIcon() {
    setIcon(null);
    setUriSmallIcon(null);
    setUriMediumIcon(null);
    setUriLargeIcon(null);
  }

  public void clearAllImages() {
    clearImageFile();
    clearSvg();
    clearIcon();
  }

  public interface ValidationPost {}

  public interface ValidationPut {}
}
