package com.ladbrokescoral.oxygen.cms.api.entity;

import static com.ladbrokescoral.oxygen.cms.api.entity.Patterns.VIP_LEVELS_INPUT_PATTERN;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.MediumImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SmallImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "banners")
@Data
@EqualsAndHashCode(callSuper = true)
public class Banner extends SortableEntity
    implements HasBrand, SmallImageAbstractMenu, MediumImageAbstractMenu {

  @JsonView(Views.GetAll.class)
  private String alt;

  @JsonView(Views.GetAll.class)
  private String brand;
  // link to sport category
  @JsonView(Views.GetAll.class)
  private ObjectId categoryId;

  @JsonView(Views.GetAll.class)
  @Transient
  private String categoryName;

  @Field("desktop_filename")
  private Filename desktopFilename;

  @Field("desktop_heightMedium")
  private String desktopHeightMedium;

  @Field("desktop_heightSmall")
  private String desktopHeightSmall;

  @Field("desktop_targetUri")
  private String desktopTargetUri;

  @Field("desktop_uriMedium")
  private String desktopUriMedium;

  @Field("desktop_uriSmall")
  private String desktopUriSmall;

  @Field("desktop_widthMedium")
  private String desktopWidthMedium;

  @Field("desktop_widthSmall")
  private String desktopWidthSmall;

  @JsonView(Views.GetAll.class)
  private Boolean disabled = false;

  private Filename filename;
  private Integer heightMedium;
  private Integer heightSmall;

  @JsonView(Views.GetAll.class)
  @NotNull
  @NotBlank
  private String imageTitle;

  @Field("imageTitle_brand")
  private String imageTitleBrand;

  @JsonView(Views.GetAll.class)
  private Boolean inApp;

  @JsonView(Views.GetAll.class)
  private String lang;

  @JsonView(Views.GetAll.class)
  private String showToCustomer;

  @JsonView(Views.GetAll.class)
  private String targetUri;

  private String uriMedium;
  private String uriSmall;

  @JsonView(Views.GetAll.class)
  @NotNull
  private Instant validityPeriodEnd;

  @JsonView(Views.GetAll.class)
  @NotNull
  private Instant validityPeriodStart;

  @JsonView(Views.GetAll.class)
  private List<Integer> vipLevels;

  @Pattern(
      regexp = VIP_LEVELS_INPUT_PATTERN,
      message =
          "Only hyphened and comma separated numbers are allowed. E.g: 1 or 1-3 or 12,3,5-1,4,7-10 or 1,2 ...")
  private String vipLevelsInput;

  private Integer widthMedium;
  private Integer widthSmall;

  @Field("desktop_enabled")
  private Boolean desktopEnabled;

  @Field("desktop_inApp")
  private Boolean desktopInApp;

  @JsonView(Views.GetAll.class)
  private Boolean enabled;

  private String signpostingEventLevel;
  private String signpostingMarketLevel;
}
