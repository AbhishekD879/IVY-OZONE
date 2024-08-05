package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.featured.aem.AemMetaConsumer;
import com.coral.oxygen.middleware.featured.aem.model.AemBannersRawKey;
import com.coral.oxygen.middleware.featured.aem.model.OfferObject;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.AemBannersConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.AemBannersConfig.SportPageId;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.output.featured.AemBannersImg;
import com.coral.oxygen.middleware.pojos.model.output.featured.AemBannersModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

@Slf4j
public class AemCarouselsProcessor implements ModuleConsumer<AemBannersModule> {

  private AemMetaConsumer aemMetaConsumer;
  @Getter private final Map<String, String> sportsCategoriesDict;
  private Map<AemBannersRawKey, List<OfferObject>> bannersBucket;

  public AemCarouselsProcessor(
      AemMetaConsumer aemMetaConsumer, Map<String, String> sportsCategoriesDict) {
    this.aemMetaConsumer = aemMetaConsumer;
    this.sportsCategoriesDict = sportsCategoriesDict;
    this.bannersBucket = Collections.emptyMap();
  }

  public boolean populateBannersBucket() {
    Map<AemBannersRawKey, List<OfferObject>> newBucket = new HashMap<>();
    List<OfferObject> offers = aemMetaConsumer.getBanners();
    if (offers.isEmpty()) {
      this.bannersBucket = Collections.emptyMap();
      return false;
    }
    offers.stream()
        .forEach(
            offer ->
                multiplyCollections(offer).entrySet().stream()
                    .forEach(
                        entity -> {
                          List<OfferObject> tmp =
                              newBucket.getOrDefault(entity.getKey(), new ArrayList<>());
                          tmp.add(entity.getValue());
                          newBucket.put(entity.getKey(), tmp);
                        }));
    if (newBucket.isEmpty()) {
      return false;
    }
    newBucket
        .entrySet()
        .forEach(
            entity ->
                entity
                    .getValue()
                    .sort((o1, o2) -> Integer.compare(o1.getDisplayOrder(), o2.getDisplayOrder())));
    this.bannersBucket = newBucket;
    return true;
  }

  /** duplicate free. */
  protected Map<AemBannersRawKey, OfferObject> multiplyCollections(final OfferObject offer) {
    if (offer == null || offer.getPages() == null) {
      return Collections.emptyMap();
    }
    Set<AemBannersRawKey> keys =
        offer.getPages().stream()
            .flatMap(
                page ->
                    offer.getCarousels().stream()
                        .map(cat -> idResolver(page, cat))
                        .filter(
                            key -> key != null && !AemBannersRawKey.UNKNOWN_PAGE_KEY.equals(key))
                        .collect(Collectors.toList())
                        .stream())
            .collect(Collectors.toSet());
    return keys.stream().collect(Collectors.toMap(key -> key, key -> offer));
  }

  protected AemBannersRawKey idResolver(String jcrPageName, String jchCarouselName) {
    if (StringUtils.isBlank(jcrPageName) || StringUtils.isBlank(jchCarouselName)) {
      return AemBannersRawKey.UNKNOWN_PAGE_KEY;
    }
    String pageName = AemBannersRawKey.stripJcrKey(jcrPageName);
    String pageId = sportsCategoriesDict.getOrDefault(pageName, pageName);
    PageType pageType = PageType.fromPageId(pageId).orElse(null);
    if (pageType == null) {
      return AemBannersRawKey.UNKNOWN_PAGE_KEY;
    }
    return AemBannersRawKey.builder()
        .carouselId(AemBannersRawKey.stripJcrKey(jchCarouselName))
        .pageId(pageId)
        .type(pageType)
        .build();
  }

  @Override
  public AemBannersModule processModule(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    if (bannersBucket.isEmpty()) {
      log.error("No banners come from AEM");
      return null;
    }
    if (moduleConfig.getPageData() == null || moduleConfig.getPageData().size() < 1) {
      log.error("Aem banners module was broken {}", moduleConfig);
      return null;
    }
    SportPageModuleDataItem item = moduleConfig.getPageData().get(0);
    if (!(item instanceof AemBannersConfig)) {
      log.error("Aem banners data item was broken {}", item);
      return null;
    }
    final AemBannersConfig aemModuleConfig = (AemBannersConfig) item;
    SportPageId pageId = aemModuleConfig.getSportPageId();
    AemBannersRawKey key = AemBannersRawKey.fromPageId(pageId);
    List<OfferObject> offers = this.getBannersForModule(key);
    if (offers.isEmpty()) {
      log.warn("No banners for apply to {}", key);
      return null;
    }
    List<AemBannersImg> images =
        offers.stream()
            // .limit(aemModuleConfig.getMaxOffers()) the limitation will be implemented in UI
            // banners carousel module.
            .map(offer -> mapToAemBannersImg(offer))
            .collect(Collectors.toList());

    if (images.isEmpty()) {
      return null;
    }
    return mapToAemBannerModel(moduleConfig.getSportModule().getId(), aemModuleConfig, images);
  }

  @Override
  public List<AemBannersModule> processModules(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    try {
      return Arrays.asList(processModule(moduleConfig, cmsSystemConfig, excludedEventIds));
    } catch (Exception e) {
      log.error("Aem banners module processor exception {} ", moduleConfig, e);
      return Collections.emptyList();
    }
  }

  private AemBannersImg mapToAemBannersImg(OfferObject offer) {
    return AemBannersImg.builder()
        .imgUrl(offer.getImgUrl())
        .altText(offer.getAltText())
        .guid(offer.getId())
        .appTarget(offer.getAppTarget())
        .offerTitle(offer.getOfferTitle())
        .offerName(offer.getOfferName())
        .imgUrl(offer.getImgUrl())
        .webUrl(offer.getWebUrl())
        .roxanneWebUrl(offer.getRoxanneWebUrl())
        .appUrl(offer.getAppUrl())
        .roxanneAppUrl(offer.getRoxanneAppUrl())
        .webTarget(offer.getWebTarget())
        .appTarget(offer.getAppTarget())
        .selectionId(offer.getSelectionId())
        .altText(offer.getAltText())
        .webTandC(offer.getWebTandC())
        .webTandCLink(offer.getWebTandCLink())
        .mobTandCLink(offer.getMobTandCLink())
        .isScrbrd(offer.getIsScrbrd())
        .scrbrdEventId(offer.getScrbrdEventId())
        .scrbrdPosition(offer.getScrbrdPosition())
        .scrbrdTypeId(offer.getScrbrdTypeId())
        .displayOrder(offer.getDisplayOrder())
        .userType(offer.getUserType())
        .imsLevel(offer.getImsLevel())
        .selectChannels(offer.getSelectChannels())
        .build();
  }

  protected static AemBannersModule mapToAemBannerModel(
      String id, AemBannersConfig aemModuleConfig, List<AemBannersImg> images) {
    return AemBannersModule.builder()
        .id(id)
        .pageType(aemModuleConfig.getSportPageId().getPageType())
        .sportId(Integer.parseInt(aemModuleConfig.getSportPageId().getId()))
        .publishedDevices(Collections.emptyList())
        .showExpanded(true)
        .data(images)
        .maxOffers(aemModuleConfig.getMaxOffers())
        .timePerSlide(aemModuleConfig.getTimePerSlide())
        .build();
  }

  protected List<OfferObject> getBannersForModule(AemBannersRawKey key) {
    return bannersBucket.getOrDefault(key, Collections.emptyList());
  }
}
