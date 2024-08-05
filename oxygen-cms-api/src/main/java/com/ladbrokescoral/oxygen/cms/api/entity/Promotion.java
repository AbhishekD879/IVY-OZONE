package com.ladbrokescoral.oxygen.cms.api.entity;

import static com.ladbrokescoral.oxygen.cms.api.entity.Patterns.VIP_LEVELS_INPUT_PATTERN;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = Promotion.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(name = "brand_promotions", def = "{'promoKey' : 1, 'brand': 1}", unique = true)
public class Promotion extends SortableEntity implements HasBrand {

  public static final String COLLECTION_NAME = "promotions";

  @NotBlank private String brand;
  private String description;
  private Boolean disabled = false;
  private Filename filename;
  private Integer heightMedium;
  private Integer heightSmall;
  private String htmlMarkup;
  private String promotionText;
  private String key;
  private String lang = "en";
  private SvgFilename previewImage;
  @NotNull private String promoKey;
  @NotNull private String shortDescription;
  @NotNull @NotBlank private String title;
  private String popupTitle;
  private String uriMedium;
  private String uriSmall;
  @NotNull private Instant validityPeriodEnd;
  @NotNull private Instant validityPeriodStart;
  private List<Integer> vipLevels;
  private Integer widthMedium;
  private Integer widthSmall;
  @NotBlank private String showToCustomer;
  private String directFileUrl;
  private Boolean useDirectFileUrl = false;
  private String requestId;
  private Boolean isSignpostingPromotion = false;

  private BetPack betPack;

  private PromoFreeRideConfig freeRideConfig;

  @Pattern(
      regexp = VIP_LEVELS_INPUT_PATTERN,
      message =
          "Only hyphened and comma separated numbers are allowed. E.g: 1 or 1-3 or 12,3,5-1,4,7-10 or 1,2 ...")
  private String vipLevelsInput;

  @JsonProperty("title_brand")
  @Field("title_brand")
  private String titleBrand;

  @NotNull private List<ObjectId> categoryId = new ArrayList<>();
  private List<String> competitionId = new ArrayList<>();
  private String eventLevelFlag;
  private String marketLevelFlag;
  private String overlayBetNowUrl;
  private String promotionId;
  private String openBetId;

  private Boolean useCustomPromotionName = false;
  private String customPromotionName;

  private String navigationGroupId;

  private String templateMarketName;
  private String blurbMessage;
}
