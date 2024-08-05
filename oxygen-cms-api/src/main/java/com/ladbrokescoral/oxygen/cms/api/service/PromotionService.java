package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class PromotionService extends SortableService<Promotion> {

  private final PromotionRepository repo;

  private final ImageService imageService;

  private final String mediumPromotionPath;
  private final String promotionImageSize;

  private final PromotionLeaderboardMsgPublishService msgPublishService;
  private final NavItemService navItemService;

  public static final String ERR_MSG =
      "Error occurred while publishing leaderboard config to kafka";

  public static final String TRY_AGAIN_MSG = " Plz try again..";

  private Map<String, String> promoDeleteMap = new HashMap<>();

  public Map<String, String> getPromoDeleteMap() {
    return promoDeleteMap;
  }

  @Autowired
  public PromotionService(
      PromotionRepository repository,
      ImageService imageService,
      @Value("${images.promotions.medium}") String mediumPromotionPath,
      @Value("${images.promotions.size}") String promotionImageSize,
      PromotionLeaderboardMsgPublishService msgPublishService,
      NavItemService navItemService) {
    super(repository);
    this.repo = repository;
    this.imageService = imageService;
    this.mediumPromotionPath = mediumPromotionPath;
    this.promotionImageSize = promotionImageSize;
    this.msgPublishService = msgPublishService;
    this.navItemService = navItemService;
  }

  public List<Promotion> findAllSorted() {
    return repo.findAll(SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public List<Promotion> findAllByBrandSorted(String brand) {
    return repo.findPromotions(brand, Instant.now(), SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public Optional<Promotion> findByBrandAndPromotionId(String brand, String promotionId) {
    return repo.findPromotionByBrandAndPromotionId(brand, promotionId);
  }

  public List<Promotion> findAllExceptPromotionIds(List<String> promotionIds) {
    return repo.findPromotionByPromotionIdNotIn(promotionIds);
  }

  /** @return list of promotions with the same order as promotionIds */
  public List<Promotion> findByPromotionIdsSorted(String brand, List<String> promotionIds) {
    return repo.findPromotionByPromotionIds(brand, Instant.now(), promotionIds).stream()
        .sorted(Comparator.comparing(p -> promotionIds.indexOf(p.getPromotionId())))
        .collect(Collectors.toList());
  }

  public List<Promotion> findByIds(String brand, List<String> ids) {
    return repo.findPromotionsByIds(brand, Instant.now(), ids);
  }

  public List<Promotion> findAllByBrandSortedAndCategoryIds(String brand, List<ObjectId> ids) {
    return repo.findPromotionsWithCategoryIds(
        brand, Instant.now(), SortableService.SORT_BY_SORT_ORDER_ASC, ids);
  }

  public List<Promotion> findAllByBrandSortedAndCompetitionId(String brand, String id) {
    return repo.findPromotionsWithCompetitionId(
        brand, Instant.now(), SortableService.SORT_BY_SORT_ORDER_ASC, id);
  }

  public Optional<Promotion> attachImage(
      Promotion promotion, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image) {

    ImageServiceImpl.Size size = new ImageServiceImpl.Size(promotionImageSize);
    Optional<Filename> uploaded =
        imageService.upload(promotion.getBrand(), image, mediumPromotionPath, size);

    return uploaded.map(
        uploadedImage -> {
          promotion.setHeightMedium(size.getHeight());
          promotion.setWidthMedium(size.getWidth());
          promotion.setUriMedium(
              PathUtil.normalizedPath(mediumPromotionPath, uploadedImage.getFilename()));
          return promotion;
        });
  }

  public Optional<Promotion> removeImage(Promotion promotion) {
    return Optional.ofNullable(promotion.getUriMedium())
        .map(
            uriMedium -> {
              Boolean isDeleted = imageService.removeImage(promotion.getBrand(), uriMedium);
              log.info(String.format("File %s removal status : %s", uriMedium, isDeleted));
              promotion.setUriMedium(null);
              promotion.setHeightMedium(null);
              promotion.setWidthMedium(null);
              return promotion;
            });
  }

  @Override
  public Promotion save(Promotion entity) {
    Promotion promotion = super.save(entity);
    try {
      if (Objects.nonNull(entity.getNavigationGroupId())
          && !"Deleted".equals(getPromoDeleteMap().get(entity.getId()))) {
        sendKafkaCreateMsgForNewLbrConfig(promotion, entity.getNavigationGroupId());
      }
    } catch (Exception ex) {
      log.error(
          ERR_MSG + " while creating promotion,promoId : {}, {}",
          entity.getPromotionId(),
          ex.getMessage());
      promotion.setNavigationGroupId(null);
      repo.save(promotion);
      throw new PromoLeaderboardException(ERR_MSG + TRY_AGAIN_MSG);
    }
    return promotion;
  }

  @Override
  public Promotion update(Promotion existingEntity, Promotion updateEntity) {
    List<NavItem> existingNavItem = new ArrayList<>();
    if (Objects.nonNull(existingEntity.getNavigationGroupId())) {
      existingNavItem =
          navItemService.getLeaderboardNavItems(existingEntity.getNavigationGroupId());
    }
    prepareModelBeforeSave(updateEntity);
    Promotion savedPromotion = repository.save(updateEntity);
    try {
      if (Objects.nonNull(updateEntity.getNavigationGroupId())) {
        if (Objects.isNull(existingEntity.getNavigationGroupId())) {
          sendKafkaCreateMsgForNewLbrConfig(savedPromotion, updateEntity.getNavigationGroupId());
        } else if (!existingEntity
            .getNavigationGroupId()
            .equals(updateEntity.getNavigationGroupId())) {

          sendKafkaCreateMsgForNewLbrConfig(savedPromotion, updateEntity.getNavigationGroupId());
          List<NavItem> distinctNavItems =
              getDistinctLeaderboard(existingNavItem, updateEntity.getNavigationGroupId());
          sendKafkaDeleteMsgForExistingPromo(distinctNavItems, savedPromotion);

        } else if (isPromoDateChange(existingEntity, updateEntity)) {
          sendKafkaPromoDateChangeMsg(savedPromotion);
        }
      } else if (Objects.nonNull(existingEntity.getNavigationGroupId())) {
        sendKafkaDeleteMsgForExistingPromo(existingNavItem, savedPromotion);
      }

    } catch (Exception ex) {
      savedPromotion.setNavigationGroupId(null);
      repository.save(savedPromotion);
      log.error(
          ERR_MSG + " while updating promotion,promoId: {},{}",
          updateEntity.getPromotionId(),
          ex.getMessage());
      throw new PromoLeaderboardException(ERR_MSG + TRY_AGAIN_MSG);
    }
    return savedPromotion;
  }

  @Override
  public void delete(String id) {
    Promotion promo = repository.findById(id).orElseThrow(NotFoundException::new);
    super.delete(id);
    try {
      if (Objects.nonNull(promo.getNavigationGroupId())) {
        List<NavItem> navItems =
            navItemService.getLeaderboardNavItems(promo.getNavigationGroupId());
        sendKafkaDeleteMsgForExistingPromo(navItems, promo);
      }
    } catch (Exception ex) {
      repo.save(promo);
      log.error(ERR_MSG + " while deleting promotion,promoId:{},{}", id, ex.getMessage());
      throw new PromoLeaderboardException(ERR_MSG + TRY_AGAIN_MSG);
    }
  }

  @Override
  public Promotion prepareModelBeforeSave(Promotion promotion) {
    promotion.setTitleBrand(generateTitleBrand(promotion));
    promotion.setVipLevels(
        !StringUtils.isBlank(promotion.getVipLevelsInput()) ? generateVipLevels(promotion) : null);
    return promotion;
  }

  public List<Promotion> findSignpostingPromotions(String brand) {
    return repo.findSignpostingPromotions(
        brand, Instant.now(), SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  private String generateTitleBrand(Promotion promotion) {
    return new StringBuilder(promotion.getTitle())
        .append("-")
        .append(promotion.getPromoKey())
        .append("-")
        .append(promotion.getBrand())
        .toString();
  }

  private List<Integer> generateVipLevels(Promotion promotion) {
    return Util.hyphenatedAndCommaSeparatedNumbersToList(promotion.getVipLevelsInput());
  }

  public Optional<Promotion> findByBrandAndPromoKey(String brand, String promoKey) {
    return repo.findPromotionByBrandAndPromoKey(brand, promoKey);
  }

  private void sendKafkaPromoDateChangeMsg(Promotion savedPromotion) {
    List<NavItem> lbrNavItems =
        navItemService.getLeaderboardNavItems(savedPromotion.getNavigationGroupId());
    if (!lbrNavItems.isEmpty()) {
      msgPublishService.publishMessage(
          PromoLbKafkaAction.PROMO_DATE_CHANGE.getValue(), savedPromotion, null);
    }
  }

  private void sendKafkaDeleteMsgForExistingPromo(
      List<NavItem> existingNavItems, Promotion savedPromotion) {
    if (!existingNavItems.isEmpty()) {
      msgPublishService.publishMessage(
          PromoLbKafkaAction.DELETE.getValue(),
          savedPromotion,
          navItemService.getLbConfigByNavItems(getLbConfigIds(existingNavItems)));
    }
  }

  private void sendKafkaCreateMsgForNewLbrConfig(Promotion savedPromotion, String navGroupId) {
    List<NavItem> updatedNavItems = navItemService.getLeaderboardNavItems(navGroupId);
    if (!updatedNavItems.isEmpty()) {
      msgPublishService.publishMessage(
          PromoLbKafkaAction.CREATE.getValue(),
          savedPromotion,
          navItemService.getLbConfigByNavItems(getLbConfigIds(updatedNavItems)));
    }
  }

  private List<String> getLbConfigIds(List<NavItem> navItems) {
    return navItems.stream().map(NavItem::getLeaderboardId).collect(Collectors.toList());
  }

  private List<NavItem> getDistinctLeaderboard(List<NavItem> existingNavItem, String navGroupId) {
    List<String> newLeaderboardIdsList =
        getLbConfigIds(navItemService.getLeaderboardNavItems(navGroupId));
    return existingNavItem.stream()
        .filter(e -> !newLeaderboardIdsList.contains(e.getLeaderboardId()))
        .collect(Collectors.toList());
  }

  private boolean isPromoDateChange(Promotion existingPromo, Promotion updatedPromo) {
    return (existingPromo.getValidityPeriodStart().getEpochSecond()
            != updatedPromo.getValidityPeriodStart().getEpochSecond())
        || (existingPromo.getValidityPeriodEnd().getEpochSecond()
            != updatedPromo.getValidityPeriodEnd().getEpochSecond());
  }
}
