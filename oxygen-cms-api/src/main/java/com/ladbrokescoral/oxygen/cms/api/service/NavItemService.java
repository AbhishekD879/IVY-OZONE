package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.NavItemDto;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoMsgLbConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.repository.NavItemRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromoLeaderboardRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class NavItemService extends SortableService<NavItem> {

  private final NavItemRepository navItemRepository;

  private final PromotionRepository promotionRepository;

  private final ModelMapper modelMapper;

  private final PromotionLeaderboardMsgPublishService msgPublishService;

  private final PromoLeaderboardRepository promoLeaderboardRepository;

  public static final String ERR_MSG = "Error occurred while publishing message to Kafka";

  public static final String TRY_AGAIN_MSG = " Plz try again..";

  public static final String LEADERBOARD_NAV_TYPE = "Leaderboard";

  private String isUpdatedCall = null;

  public NavItemService(
      NavItemRepository navItemRepository,
      PromotionRepository promotionRepository,
      ModelMapper modelMapper,
      PromotionLeaderboardMsgPublishService msgPublishService,
      PromoLeaderboardRepository promoLeaderboardRepository) {
    super(navItemRepository);
    this.navItemRepository = navItemRepository;
    this.promotionRepository = promotionRepository;
    this.modelMapper = modelMapper;
    this.msgPublishService = msgPublishService;
    this.promoLeaderboardRepository = promoLeaderboardRepository;
  }

  @Override
  public NavItem save(NavItem entity) {
    if (entity.getSortOrder() == null) {
      Double sortedOrder = findMinSortedOrder(entity.getNavigationGroupId()) - SORT_ORDER_STEP;
      entity.setSortOrder(sortedOrder);
    }
    NavItem navItem = super.save(entity);
    if (Objects.isNull(isUpdatedCall)) {
      sendKafkaCreateMsg(navItem);
    }
    return navItem;
  }

  private void sendKafkaCreateMsg(NavItem entity) {
    List<Promotion> promotions =
        getAllLinkedPromotionByNavGroupsId(
            Collections.singletonList(entity.getNavigationGroupId()));
    try {
      if (!promotions.isEmpty() && LEADERBOARD_NAV_TYPE.equalsIgnoreCase(entity.getNavType())) {
        for (Promotion promotion : promotions) {
          msgPublishService.publishMessage(
              PromoLbKafkaAction.CREATE.getValue(),
              promotion,
              getLbConfigByNavItems(Collections.singletonList(entity.getLeaderboardId())));
        }
      }
    } catch (Exception ex) {
      log.error(ERR_MSG + " on navItem create navId: {},{}", entity.getId(), ex.getMessage());
      throw new PromoLeaderboardException(ERR_MSG);
    }
  }

  private Double findMinSortedOrder(String id) {
    Optional<NavItem> navItem =
        navItemRepository
            .findAllNavItemByNavigationGroupId(id, SortableService.SORT_BY_SORT_ORDER_ASC).stream()
            .findFirst();
    if (navItem.isPresent()) {
      return navItem.get().getSortOrder();
    } else {
      return 0d;
    }
  }

  public Optional<NavigationGroupDto> findNavigationGroup(
      String id, Optional<NavigationGroup> navigationGroup) {

    // Fetching all Promotions linked to this NavGrp whether expired or not
    List<String> promoIds =
        promotionRepository.findAllByNavigationGroupIdIn(Collections.singletonList(id)).stream()
            .map(AbstractEntity::getId)
            .collect(Collectors.toList());

    List<NavItem> sortedNavItems =
        navItemRepository.findAllNavItemByNavigationGroupId(
            id, SortableService.SORT_BY_SORT_ORDER_ASC);

    Map<String, Boolean> lbrMap =
        promoLeaderboardRepository.findAllByIdIn(getLbrIds(sortedNavItems)).stream()
            .collect(
                Collectors.toMap(PromoLeaderboardConfig::getId, PromoLeaderboardConfig::getStatus));
    return navigationGroup
        .map(e -> modelMapper.map(e, NavigationGroupDto.class))
        .flatMap(
            (NavigationGroupDto navigationGroupDto) -> {
              navigationGroupDto.setNavItems(
                  sortedNavItems.stream()
                      .map(e -> modelMapper.map(e, NavItemDto.class))
                      .map(
                          (NavItemDto navItemDto) -> {
                            navItemDto.setLeaderboardStatus(
                                lbrMap.getOrDefault(navItemDto.getLeaderboardId(), null));
                            return navItemDto;
                          })
                      .collect(Collectors.toList()));
              navigationGroupDto.setPromotionIds(
                  !promoIds.isEmpty() ? promoIds : new ArrayList<>());
              return Optional.of(navigationGroupDto);
            });
  }

  @Override
  public NavItem update(NavItem existingEntity, NavItem updateEntity) {
    this.isUpdatedCall = "yes";
    super.update(existingEntity, updateEntity);
    this.isUpdatedCall = null;
    try {
      List<Promotion> promotions =
          getAllLinkedPromotionByNavGroupsId(
              Collections.singletonList(existingEntity.getNavigationGroupId()));
      if (isRddDeletionRqd(existingEntity.getNavType(), updateEntity.getNavType())) {
        for (Promotion promotion : promotions) {
          msgPublishService.publishMessage(
              PromoLbKafkaAction.DELETE.getValue(),
              promotion,
              Collections.singletonList(
                  new PromoMsgLbConfigDto(existingEntity.getLeaderboardId())));
        }
      }

      if (isRddCreationRqd(existingEntity.getNavType(), updateEntity.getNavType())) {
        for (Promotion promotion : promotions) {
          msgPublishService.publishMessage(
              PromoLbKafkaAction.CREATE.getValue(),
              promotion,
              getLbConfigByNavItems(Collections.singletonList(updateEntity.getLeaderboardId())));
        }
      }
    } catch (Exception ex) {
      log.error(ERR_MSG + " on navItem update navId: {},{}", updateEntity.getId(), ex.getMessage());
      throw new PromoLeaderboardException(ERR_MSG + TRY_AGAIN_MSG);
    }
    return updateEntity;
  }

  @Override
  public void delete(String id) {
    try {
      NavItem navItem = navItemRepository.findById(id).orElseThrow(NotFoundException::new);
      if (LEADERBOARD_NAV_TYPE.equalsIgnoreCase(navItem.getNavType())) {
        List<Promotion> promotionList =
            getAllLinkedPromotionByNavGroupsId(
                Collections.singletonList(navItem.getNavigationGroupId()));
        for (Promotion promotion : promotionList) {
          msgPublishService.publishMessage(
              PromoLbKafkaAction.DELETE.getValue(),
              promotion,
              Collections.singletonList(new PromoMsgLbConfigDto(navItem.getLeaderboardId())));
        }
      }
    } catch (Exception ex) {
      log.error(ERR_MSG + " on NavItem delete. navId : {},{}", id, ex.getMessage());
      throw new PromoLeaderboardException(ERR_MSG + TRY_AGAIN_MSG);
    }
    super.delete(id);
  }

  public List<NavItem> getLeaderboardNavItems(String navigationId) {
    return navItemRepository.findAllNavItemByNavTypeEqualsIgnoreCaseAndNavigationGroupId(
        LEADERBOARD_NAV_TYPE, navigationId);
  }

  public List<NavItem> getNavItemWithActiveLbr(List<NavItem> navItems) {
    List<String> activePromoLeaderboardIds =
        promoLeaderboardRepository.findAllByIdIn(getLbrIds(navItems)).stream()
            .filter(PromoLeaderboardConfig::getStatus)
            .map(PromoLeaderboardConfig::getId)
            .collect(Collectors.toList());
    return navItems.stream()
        .filter(
            navItem ->
                Objects.isNull(navItem.getLeaderboardId())
                    || activePromoLeaderboardIds.contains(navItem.getLeaderboardId()))
        .collect(Collectors.toList());
  }

  private List<String> getLbrIds(List<NavItem> navItems) {
    return navItems.stream()
        .map(NavItem::getLeaderboardId)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  public List<Promotion> getAllLinkedPromotionByNavGroupsId(List<String> navGIds) {
    return promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
        navGIds, Instant.now());
  }

  public List<PromoMsgLbConfigDto> getLbConfigByNavItems(List<String> leaderboardIdList) {
    List<PromoMsgLbConfigDto> msgLbConfigDtoList = new ArrayList<>();
    promoLeaderboardRepository
        .findAllById(leaderboardIdList)
        .forEach(
            (PromoLeaderboardConfig promoLbConfigs) -> {
              PromoMsgLbConfigDto promoMsConfigDto = new PromoMsgLbConfigDto();
              promoMsConfigDto.setLeaderboardId(promoLbConfigs.getId());
              promoMsConfigDto.setFilePath(promoLbConfigs.getFilePath());
              msgLbConfigDtoList.add(promoMsConfigDto);
            });
    return msgLbConfigDtoList;
  }

  private boolean isRddDeletionRqd(String existingNavType, String updatedNavType) {
    return (LEADERBOARD_NAV_TYPE.equalsIgnoreCase(existingNavType)
            && !LEADERBOARD_NAV_TYPE.equalsIgnoreCase(updatedNavType))
        || (isLbNavItemUpdated(existingNavType, updatedNavType));
  }

  private boolean isRddCreationRqd(String existingNavType, String updatedNavType) {
    return (!LEADERBOARD_NAV_TYPE.equalsIgnoreCase(existingNavType)
            && LEADERBOARD_NAV_TYPE.equalsIgnoreCase(updatedNavType))
        || (isLbNavItemUpdated(existingNavType, updatedNavType));
  }

  private boolean isLbNavItemUpdated(String existingNavType, String updatedNavType) {
    return LEADERBOARD_NAV_TYPE.equalsIgnoreCase(existingNavType)
        && LEADERBOARD_NAV_TYPE.equalsIgnoreCase(updatedNavType);
  }

  public void deleteAllNavItems(List<NavItem> navItems) {
    navItemRepository.deleteAll(navItems);
  }

  public List<NavItem> findAllNavItemsByLbId(String leaderboardID) {
    return navItemRepository.findAllNavItemByLeaderboardId(leaderboardID);
  }

  public List<NavItem> findAllNavItem(String brand) {
    return navItemRepository.findAllNavItemByBrand(brand);
  }

  public List<NavItem> findAllNavItemByBrandWhereLbrIdNotNull(String brand) {
    return navItemRepository.findAllByBrandAndLeaderboardIdNotNull(brand);
  }
}
