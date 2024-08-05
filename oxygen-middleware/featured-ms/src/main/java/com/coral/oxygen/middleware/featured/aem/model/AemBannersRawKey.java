package com.coral.oxygen.middleware.featured.aem.model;

import com.coral.oxygen.middleware.pojos.model.cms.featured.AemBannersConfig;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageKey;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.util.Objects;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;

/** This index a support recall paradigm. */
@Getter
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true, includeFieldNames = true)
public class AemBannersRawKey extends PageKey {

  public static final String CAROUSEL_PREFIX = "carousel";

  public static final AemBannersRawKey UNKNOWN_PAGE_KEY =
      new AemBannersRawKey(null, null, null) {

        @Override
        public boolean equals(Object o) {
          if (this == o) {
            return true;
          }
          if (!(o instanceof AemBannersRawKey)) {
            return false;
          }
          AemBannersRawKey otherKey = (AemBannersRawKey) o;
          if (otherKey.getType() == null || otherKey.getType().equals(PageType.unknownPage)) {
            return true;
          }
          if (otherKey.carouselId == null || otherKey.getPageId() == null) {
            return true;
          }
          return super.equals(o);
        }

        @Override
        public int hashCode() {
          return 0;
        }
      };

  private final String carouselId;

  public static class AemBannersRawKeyBuilder {
    public AemBannersRawKeyBuilder sportPageId(AemBannersConfig.SportPageId sportPageId) {
      this.type = sportPageId.getPageType();
      this.pageId = this.type.getPrefix() + sportPageId.getId();
      return this;
    }
  }

  @Builder
  public AemBannersRawKey(PageType type, String pageId, String carouselId) {
    super(type, pageId);
    this.carouselId = carouselId;
  }

  /**
   * @param jcrKey mask -> domain:rootNode/key
   */
  public static String stripJcrKey(String jcrKey) {
    return jcrKey.substring(jcrKey.indexOf('/') + 1);
  }

  public static AemBannersRawKey fromPageId(AemBannersConfig.SportPageId sportPageId) {
    return AemBannersRawKey.builder()
        .sportPageId(sportPageId)
        .carouselId(CAROUSEL_PREFIX + sportPageId.getModuleDataId().toString())
        .build();
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof AemBannersRawKey)) {
      return false;
    }
    if (!super.equals(o)) {
      return false;
    }
    AemBannersRawKey that = (AemBannersRawKey) o;
    return getCarouselId().equals(that.getCarouselId());
  }

  @Override
  public int hashCode() {
    return Objects.hash(super.hashCode(), getCarouselId());
  }
}
