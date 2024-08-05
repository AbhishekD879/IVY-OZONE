package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoLeaderboardConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoMsgLbConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.repository.PromoLeaderboardRepository;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class PromoLeaderboardService extends AbstractService<PromoLeaderboardConfig> {

  private final PromotionLeaderboardMsgPublishService msgPublishService;

  private final NavItemService navItemService;

  private final ModelMapper modelMapper;

  public static final String ERR_MSG = "Error occurred while publishing message to Kafka ";

  public static final String TRY_AGAIN_MSG = " Plz try again..";

  private Map<String, Boolean> fileChangedMap = new HashMap<>();

  public Map<String, Boolean> getFileChangedMap() {
    return fileChangedMap;
  }

  public PromoLeaderboardService(
      PromoLeaderboardRepository promoLeaderboardRepository,
      PromotionLeaderboardMsgPublishService msgPublishService,
      NavItemService navItemService,
      ModelMapper modelMapper) {
    super(promoLeaderboardRepository);
    this.msgPublishService = msgPublishService;
    this.navItemService = navItemService;
    this.modelMapper = modelMapper;
  }

  @Override
  public PromoLeaderboardConfig update(
      PromoLeaderboardConfig existingEntity, PromoLeaderboardConfig updateEntity) {
    super.update(existingEntity, updateEntity);
    try {
      if (Boolean.TRUE.equals(getFileChangedMap().get(updateEntity.getId()))) {
        List<NavItem> navItems = navItemService.findAllNavItemsByLbId(updateEntity.getId());
        List<Promotion> promotions =
            navItemService.getAllLinkedPromotionByNavGroupsId(getMappedNavGroupIds(navItems));
        for (Promotion promotion : promotions) {
          msgPublishService.publishMessage(
              PromoLbKafkaAction.UPDATE.getValue(),
              promotion,
              Collections.singletonList(convertEntityToDto(updateEntity)));
        }
      }
    } catch (Exception ex) {
      log.error(
          ERR_MSG + " on leaderboardConfig update,leaderboardId:{},{}",
          updateEntity.getId(),
          ex.getMessage());
      throw new PromoLeaderboardException(ERR_MSG + TRY_AGAIN_MSG);
    }
    return updateEntity;
  }

  @Override
  public void delete(String id) {
    List<NavItem> navItems = navItemService.findAllNavItemsByLbId(id);
    try {
      navItemService.deleteAllNavItems(navItems);
    } catch (Exception ex) {
      log.error(
          "Error while deleting Nav item linked to this LeaderboardId : {} : {}",
          id,
          ex.getMessage());
      throw new PromoLeaderboardException("Error while deleting Nav item.plz try again..");
    }
    List<Promotion> promotions =
        navItemService.getAllLinkedPromotionByNavGroupsId(getMappedNavGroupIds(navItems));
    try {
      for (Promotion promotion : promotions) {
        msgPublishService.publishMessage(
            PromoLbKafkaAction.DELETE.getValue(),
            promotion,
            Collections.singletonList(new PromoMsgLbConfigDto(id)));
      }
    } catch (Exception ex) {
      log.error(ERR_MSG + " on leaderboardConfig delete,leaderboardId:{},{}", id, ex.getMessage());
      throw new PromoLeaderboardException(ERR_MSG + TRY_AGAIN_MSG);
    }
    super.delete(id);
  }

  public List<PromoLeaderboardConfigDto> findLeaderboardByBrand(String brand) {
    Map<String, Set<String>> lbNavGIdMap =
        navItemService.findAllNavItemByBrandWhereLbrIdNotNull(brand).stream()
            .collect(
                Collectors.groupingBy(
                    NavItem::getLeaderboardId,
                    Collectors.mapping(NavItem::getNavigationGroupId, Collectors.toSet())));
    return repository.findByBrand(brand).stream()
        .map(e -> modelMapper.map(e, PromoLeaderboardConfigDto.class))
        .map(
            (PromoLeaderboardConfigDto promoLeaderboardConfigDto) -> {
              if (Boolean.TRUE.equals(promoLeaderboardConfigDto.getStatus())) {
                promoLeaderboardConfigDto.setNavGIds(
                    String.join(
                        "|",
                        lbNavGIdMap.getOrDefault(
                            promoLeaderboardConfigDto.getId(), new HashSet<>())));
              }
              return promoLeaderboardConfigDto;
            })
        .collect(Collectors.toList());
  }

  private List<String> getMappedNavGroupIds(List<NavItem> navItems) {
    return navItems.stream()
        .map(NavItem::getNavigationGroupId)
        .distinct()
        .collect(Collectors.toList());
  }

  public List<PromoLeaderboardConfigDto> findAllActiveLeaderboardByBrand(String brand) {
    return repository.findByBrand(brand).stream()
        .filter(PromoLeaderboardConfig::getStatus)
        .map(
            promoConfig ->
                new PromoLeaderboardConfigDto(promoConfig.getId(), promoConfig.getName()))
        .collect(Collectors.toList());
  }

  private PromoMsgLbConfigDto convertEntityToDto(PromoLeaderboardConfig updateEntity) {
    PromoMsgLbConfigDto promoMsgLbConfig = new PromoMsgLbConfigDto();
    promoMsgLbConfig.setLeaderboardId(updateEntity.getId());
    promoMsgLbConfig.setFilePath(updateEntity.getFilePath());
    return promoMsgLbConfig;
  }
}
