package com.coral.oxygen.middleware.featured.aem.model;

import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.function.Predicate;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.StringUtils;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OfferObject {

  // Tag Names
  public static final String NS_LADBROKES = "ladbrokes";
  public static final String NS_CORAL = "coral";

  public static final List<String> BRANDS_SUPPORTED =
      Collections.unmodifiableList(Arrays.asList(NS_CORAL, NS_LADBROKES));

  public static enum Fields {
    BRAND_KEY("lc", "lc", "lc", 2),
    BRAND_VALUE(BRAND_KEY, (BRANDS_SUPPORTED::contains)),
    ENDPOINT("offers.json", null, null, 4),
    LOCALE_KEY("locale", null, null, 5),
    LOCALE_VALUE(LOCALE_KEY),
    CHANNELS_KEY("channels", "selectChannels", "channels", 7),
    CHANNELS_VALUE(CHANNELS_KEY),
    PAGES_KEY("pages", "pageTags", "allowed-pages", 9),
    PAGES_VALUE(PAGES_KEY),
    USER_TYPE_KEY("userType", "userType", "customer-type", 11),
    USER_TYPE_VALUE(USER_TYPE_KEY),
    IMS_LEVEL_KEY("imsLevel", "customerSegmentstags", "ims-levels", -1),
    IMS_LEVEL_VALUE(IMS_LEVEL_KEY),
    CAROUSEL_KEY("carousels", "carousels", "carousels", -1),
    CAROUSEL_VALUE(CAROUSEL_KEY),
    ;

    private final String nodeKey;
    private final String jcrKey;
    private final Fields parent;
    private final String key;
    private final int offset; // -1 means optional value
    private Predicate<String> validator = (x -> StringUtils.isNotBlank(x));

    Fields(String urlKey, String jcrKey, String nodeKey, int offset) {
      this.key = urlKey;
      this.offset = offset;
      this.parent = null;
      this.jcrKey = jcrKey;
      this.nodeKey = nodeKey;
    }

    Fields(Fields parent) {
      this(parent, (x -> StringUtils.isNotBlank(x)));
    }

    Fields(Fields parent, Predicate<String> validator) {
      this.key = this.name();
      this.jcrKey = this.name();
      this.nodeKey = this.name();

      this.validator = validator;
      this.parent = parent;
      this.offset = -1;
    }

    public boolean isValid(String value) {
      return validator.test(value);
    }

    public String key() {
      return key;
    }

    public Fields parent() {
      return parent;
    }

    public String jcrKey() {
      return jcrKey;
    }

    public String nodeKey() {
      return nodeKey;
    }

    public int offset() {
      return offset;
    }
  }

  private String id;
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
  private Collection<String> pages;
  private Collection<String> carousels;
  private int displayOrder;
  private String startDate;
  private String endDate;
  private Set<String> imsLevel;
  private Set<String> userType;
  private Set<String> selectChannels;
}
