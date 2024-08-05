package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.pojos.model.cms.SportItem;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbonItem;
import com.newrelic.api.agent.NewRelic;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportsRibbonService {

  enum EventType {
    LIVE_EVENT,
    UPCOMING_EVENT,
    STREAM_EVENT,
    UPCOMING_STREAM_EVENT
  }

  private static final Comparator<SportsRibbonItem> itemsComparator =
      Comparator.<SportsRibbonItem, Boolean>comparing(
              item -> item.getCategoryId() == 0, Comparator.reverseOrder())
          .thenComparing(
              SportsRibbonItem::getHasLiveNow, Comparator.nullsLast(Comparator.reverseOrder()))
          .thenComparing(
              SportsRibbonItem::getDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder()))
          .thenComparing(
              SportsRibbonItem::getCategoryName, Comparator.nullsLast(Comparator.naturalOrder()));
  public static final String ALL_SPORTS = "ALL_SPORTS";

  /**
   * Analyze InPlaydata and extract SportsRibbon
   *
   * <p>Only sports with events will be present in SportRibbon
   */
  public SportsRibbon createSportsRibbon(
      List<SportItem> activeSportCategories, InPlayData inPlayData) {
    SportsRibbon result = new SportsRibbon();

    // create ribbon items from sport items (both categories and olympics)
    List<SportsRibbonItem> ribbonItems =
        activeSportCategories.stream()
            .map(this::mapSportItemToSportRibbonItem)
            .collect(Collectors.toList());

    Map<Integer, SportsRibbonItem> itemsMap = new HashMap<>();
    collectSportsRibbonItemsWithEventsToMap(
        inPlayData.getLivenow(), itemsMap, EventType.LIVE_EVENT);
    collectSportsRibbonItemsWithEventsToMap(
        inPlayData.getUpcoming(), itemsMap, EventType.UPCOMING_EVENT);
    collectSportsRibbonItemsWithEventsToMap(
        inPlayData.getLiveStream(), itemsMap, EventType.STREAM_EVENT);
    collectSportsRibbonItemsWithEventsToMap(
        inPlayData.getUpcomingLiveStream(), itemsMap, EventType.UPCOMING_STREAM_EVENT);

    ribbonItems.removeIf(
        item ->
            item.getCategoryId() != 0 && !itemsMap.containsKey(item.getCategoryId())
                || item.getCategoryId() == 0
                    && !ALL_SPORTS.equalsIgnoreCase(item.getSsCategoryCode()));

    ribbonItems.stream()
        .filter(item -> itemsMap.containsKey(item.getCategoryId()))
        .forEach(
            item -> {
              SportsRibbonItem fromModel = itemsMap.get(item.getCategoryId());
              item.setCategoryCode(fromModel.getCategoryCode());
              item.setCategoryName(fromModel.getCategoryName());
              item.setDisplayOrder(fromModel.getDisplayOrder());
              item.setHasLiveNow(fromModel.getHasLiveNow());
              item.setHasUpcoming(fromModel.getHasUpcoming());
              item.setHasLiveStream(fromModel.getHasLiveStream());
              item.setHasUpcommingLiveStream(fromModel.getHasUpcommingLiveStream());
              item.setLiveEventCount(fromModel.getLiveEventCount());
              item.setUpcomingEventCount(fromModel.getUpcomingEventCount());
              item.setLiveStreamEventCount(fromModel.getLiveStreamEventCount());
              item.setUpcommingLiveStreamEventCount(fromModel.getUpcommingLiveStreamEventCount());
            });

    Optional<SportsRibbonItem> allSportsOptional =
        ribbonItems.stream()
            .filter(item -> ALL_SPORTS.equalsIgnoreCase(item.getSsCategoryCode()))
            .findAny();
    if (allSportsOptional.isPresent()) {
      SportsRibbonItem allSports = allSportsOptional.get();
      allSports.setHasLiveNow(
          ribbonItems.stream().anyMatch(item -> item != allSports && item.getHasLiveNow()));
      allSports.setHasUpcoming(
          ribbonItems.stream().anyMatch(item -> item != allSports && item.getHasUpcoming()));
      allSports.setHasLiveStream(
          ribbonItems.stream().anyMatch(item -> item != allSports && item.getHasLiveStream()));
      allSports.setHasUpcommingLiveStream(
          ribbonItems.stream()
              .anyMatch(item -> item != allSports && item.getHasUpcommingLiveStream()));
      allSports.setLiveEventCount(
          ribbonItems.stream()
              .filter(item -> item != allSports)
              .mapToInt(SportsRibbonItem::getLiveEventCount)
              .sum());
      allSports.setUpcomingEventCount(
          ribbonItems.stream()
              .filter(item -> item != allSports)
              .mapToInt(SportsRibbonItem::getUpcomingEventCount)
              .sum());
      allSports.setLiveStreamEventCount(
          ribbonItems.stream()
              .filter(item -> item != allSports)
              .mapToInt(SportsRibbonItem::getLiveStreamEventCount)
              .sum());
      allSports.setUpcommingLiveStreamEventCount(
          ribbonItems.stream()
              .filter(item -> item != allSports)
              .mapToInt(SportsRibbonItem::getUpcommingLiveStreamEventCount)
              .sum());
    }

    ribbonItems.sort(itemsComparator);
    result.setItems(ribbonItems);
    return result;
  }

  private SportsRibbonItem mapSportItemToSportRibbonItem(SportItem sportItem) {
    SportsRibbonItem result = new SportsRibbonItem();
    try {
      result.setCategoryId(Integer.parseInt(sportItem.getCategoryId()));
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.warn("Error parsing categoryId for sports ribbon. Set to 0", e);
      result.setCategoryId(0);
    }

    result.setAlt(sportItem.getAlt());
    result.setDefaultTab(sportItem.getDefaultTab());
    result.setDisabled(sportItem.isDisabled());
    result.setDispSortName(sportItem.getDispSortName());
    result.setFileName(sportItem.getFileName());
    result.setHeightMedium(sportItem.getHeightMedium());
    result.setHeightSmall(sportItem.getWidthSmall());
    result.setImageTitle(sportItem.getImageTitle());
    result.setInApp(sportItem.getInApp());
    result.setIsMultiTemplateSport(sportItem.getMultiTemplateSport());
    result.setIsOutrightSport(sportItem.getOutrightSport());
    result.setOddsCardHeaderType(sportItem.getOddsCardHeaderType());
    result.setPrimaryMarkets(sportItem.getPrimaryMarkets());
    result.setShowInPlay(sportItem.isShowInPlay());
    result.setSsCategoryCode(sportItem.getSsCategoryCode());
    result.setSvgId(sportItem.getSvgId());
    result.setTabs(sportItem.getTabs());
    result.setTargetUri(calculateTargetUri(sportItem.getTargetUri()));
    result.setTargetUriCopy(sportItem.getTargetUri());
    result.setTypeIds(sportItem.getTypeIds());
    result.setUriMedium(sportItem.getUriMedium());
    result.setUriMediumIcon(sportItem.getUriMediumIcon());
    result.setUriSmall(sportItem.getUriSmall());
    result.setUriSmallIcon(sportItem.getUriSmallIcon());
    result.setViewByFilters(sportItem.getViewByFilters());
    result.setWidthMedium(sportItem.getWidthMedium());
    result.setWidthSmall(sportItem.getWidthSmall());

    return result;
  }

  private String calculateTargetUri(String targetUri) {
    if (Objects.isNull(targetUri)) {
      return null;
    }
    return createTargetUri(0, targetUri);
  }

  private String createTargetUri(int index, String targetUri) {
    return "#/in-play/" + targetUri.substring(index);
  }

  private void collectSportsRibbonItemsWithEventsToMap(
      InPlayModel model, Map<Integer, SportsRibbonItem> itemsMap, EventType eventType) {
    model.getSportEvents().stream()
        .filter(
            sport ->
                sport.getEventsByTypeName().stream().anyMatch(type -> !type.getEvents().isEmpty()))
        .forEach(sport -> fillOrCreateSportRibbonItem(sport, itemsMap, eventType));
  }

  /**
   * If SportsRibbonItem is not presented in itemsMap (by code) then new SportsRibbonItem will be
   * created and added to map and returned
   *
   * <p>Item hasLiveNow will be set to true if liveNow parameter is true or item hasLiveNow will be
   * set to true if liveNow parameter is false
   */
  private SportsRibbonItem fillOrCreateSportRibbonItem(
      SportSegment segment, Map<Integer, SportsRibbonItem> itemsMap, EventType eventType) {
    Integer categoryId = segment.getCategoryId();
    SportsRibbonItem item =
        itemsMap.computeIfAbsent(
            categoryId,
            key ->
                new SportsRibbonItem()
                    .setCategoryId(key)
                    .setCategoryCode(segment.getCategoryCode())
                    .setCategoryName(segment.getCategoryName())
                    .setDisplayOrder(segment.getDisplayOrder()));
    if (eventType == EventType.LIVE_EVENT) {
      item.setHasLiveNow(true);
      item.setLiveEventCount(segment.getEventCount());
    } else if (eventType == EventType.UPCOMING_EVENT) {
      item.setHasUpcoming(true);
      item.setUpcomingEventCount(segment.getEventCount());
    } else if (eventType == EventType.STREAM_EVENT) {
      item.setHasLiveStream(true);
      item.setLiveStreamEventCount(segment.getEventCount());
    } else if (eventType == EventType.UPCOMING_STREAM_EVENT) {
      item.setHasUpcommingLiveStream(true);
      item.setUpcommingLiveStreamEventCount(segment.getEventCount());
    }
    return item;
  }
}
