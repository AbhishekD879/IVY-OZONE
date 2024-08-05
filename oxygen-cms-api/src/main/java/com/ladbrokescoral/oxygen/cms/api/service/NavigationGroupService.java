package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoMsgLbConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.repository.NavItemRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationGroupRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class NavigationGroupService extends AbstractService<NavigationGroup> {

  private final NavigationGroupRepository navigationGroupRepository;
  private final PromotionRepository promotionRepository;
  private final NavItemRepository navItemRepository;
  private final ModelMapper modelMapper;
  private final NavItemService navItemService;
  private final PromotionLeaderboardMsgPublishService msgPublishService;

  public NavigationGroupService(
      NavigationGroupRepository navigationGroupRepository,
      PromotionRepository promotionRepository,
      NavItemRepository navItemRepository,
      ModelMapper modelMapper,
      NavItemService navItemService,
      PromotionLeaderboardMsgPublishService msgPublishService) {
    super(navigationGroupRepository);
    this.navigationGroupRepository = navigationGroupRepository;
    this.promotionRepository = promotionRepository;
    this.navItemRepository = navItemRepository;
    this.modelMapper = modelMapper;
    this.navItemService = navItemService;
    this.msgPublishService = msgPublishService;
  }

  public List<NavigationGroupDto> findAllNavigationGroup(String brand) {
    List<NavigationGroup> navigationGroupList = navigationGroupRepository.findByBrand(brand);

    List<Promotion> promotionList =
        promotionRepository.findAllByNavigationGroupIdIn(
            navigationGroupList.stream().map(NavigationGroup::getId).collect(Collectors.toList()));

    Map<String, List<String>> promoNavigationMap = new HashMap<>();

    promotionList.forEach(
        (Promotion promotion) ->
            promoNavigationMap
                .computeIfAbsent(promotion.getNavigationGroupId(), p -> new ArrayList<>())
                .add(promotion.getId()));

    return navigationGroupList.stream()
        .map(e -> modelMapper.map(e, NavigationGroupDto.class))
        .map(
            (NavigationGroupDto navigationGroupDto) -> {
              navigationGroupDto.setPromotionIds(
                  promoNavigationMap.getOrDefault(navigationGroupDto.getId(), new ArrayList<>()));
              return navigationGroupDto;
            })
        .collect(Collectors.toList());
  }

  public List<NavigationGroupDto> findAllActiveNavigationGroup(String brand) {
    return navigationGroupRepository.findByBrand(brand).stream()
        .filter(NavigationGroup::getStatus)
        .map(
            (NavigationGroup navigationGroup) -> {
              NavigationGroupDto groupDto = new NavigationGroupDto();
              groupDto.setId(navigationGroup.getId());
              groupDto.setTitle(navigationGroup.getTitle());
              groupDto.setStatus(navigationGroup.getStatus());
              return groupDto;
            })
        .collect(Collectors.toList());
  }

  public List<NavigationGroup> findAllActiveNavigationGroupByBrand(String brand) {
    return navigationGroupRepository.findAllNavigationGroupByBrandAndStatusIsTrue(brand);
  }

  public void deleteNavItemsByNavGId(String promotionIds, String navigationGroupId) {
    if (!promotionIds.trim().isEmpty()) {
      Iterable<Promotion> promotionList =
          promotionRepository.findAllById(Arrays.asList(promotionIds.split(",")));
      List<PromoMsgLbConfigDto> leaderboardIds =
          navItemService.getLeaderboardNavItems(navigationGroupId).stream()
              .map(navItem -> new PromoMsgLbConfigDto(navItem.getLeaderboardId()))
              .collect(Collectors.toList());
      promotionList.forEach(promotion -> promotion.setNavigationGroupId(null));
      try {
        if (!leaderboardIds.isEmpty()) {
          promotionList.forEach(
              (Promotion promotion) ->
                  msgPublishService.publishMessage(
                      PromoLbKafkaAction.DELETE.getValue(), promotion, leaderboardIds));
        }
      } catch (Exception ex) {
        log.error(
            "Error in publishing message to Kafka while deleting Navigation Group: {}",
            ex.getMessage());
        throw new PromoLeaderboardException(
            "Error while publishing message to Kafka,plz try gain..");
      }
      promotionRepository.saveAll(promotionList);
      log.info("Updated PromotionList with NavGroupId as null: {}", promotionList);
    }
    navItemRepository.deleteByNavigationGroupId(navigationGroupId);
    log.info("Deleted Nav Item corresponding to Navigation Group ID : {}", navigationGroupId);
  }

  public Optional<NavigationGroupDto> findNavigationGroup(
      String id, Optional<NavigationGroup> navigationGroup) {
    return navItemService.findNavigationGroup(id, navigationGroup);
  }
}
