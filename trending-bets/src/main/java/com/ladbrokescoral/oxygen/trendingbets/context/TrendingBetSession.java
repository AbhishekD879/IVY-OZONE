package com.ladbrokescoral.oxygen.trendingbets.context;

import com.ladbrokescoral.oxygen.trendingbets.dto.PopularBets;
import com.ladbrokescoral.oxygen.trendingbets.model.PersonalizedBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import com.ladbrokescoral.oxygen.trendingbets.service.LiveUpdatesService;
import com.ladbrokescoral.oxygen.trendingbets.util.TrendingBetsUtil;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.CollectionUtils;

@Slf4j
@Data
@RequiredArgsConstructor
public class TrendingBetSession {
  private final LiveUpdatesService liveUpdatesService;
  private final String channelId;
  private final Date latestUpdate;
  private final PopularBets betType;

  private TreeSet<TrendingPosition> positions = new TreeSet<>();
  // Contains New selections received in payload comparing to previous payload
  // (sport/mostBacked/eventStarts)
  private List<TrendingEvent> newSelections = new ArrayList<>();
  // Contains Selections which are present previous payload but not in current

  private Set<TrendingPosition> existingPositions = new HashSet<>();

  private AtomicBoolean isChanged = new AtomicBoolean(false);

  private boolean outDatedPayload;

  private TreeSet<TrendingPosition> fzYourTeamPositions = new TreeSet<>();

  private TreeSet<TrendingPosition> fzOtherTeamPositions = new TreeSet<>();

  private boolean isNewUser;

  public void updateSelectionChannels() {
    addSelectionChannelsForNewSelection();
    removeSelectionChannelsForExistingPostions();
  }

  public void updateRanksOfPositions() {
    int rank = 1;
    for (TrendingPosition position : positions) {
      position.setRank(rank++);
      isChanged.set(isPositionChanged(position));
    }
  }

  private boolean isPositionChanged(TrendingPosition position) {
    return isChanged.get() || (position.getPreviousRank() != position.getRank());
  }
  /** Updates Channel mapping for each selection and subscribe/unsubscribe if necessary. */
  private void addSelectionChannelsForNewSelection() {

    newSelections.forEach(
        (TrendingEvent selection) -> {
          TrendingBetsContext.getSelectionMappings()
              .computeIfAbsent(selection, s -> ConcurrentHashMap.newKeySet())
              .add(channelId);
          liveUpdatesService.subscriberForEvent(selection.getStreamChannels(), selection.getId());
        });
  }

  public void subscribeToLiveServer() {
    newSelections.forEach(
        (TrendingEvent selection) ->
            liveUpdatesService.subscriberForEvent(
                selection.getStreamChannels(), selection.getId()));
  }

  private void removeSelectionChannelsForExistingPostions() {
    if (CollectionUtils.isEmpty(existingPositions)) return;

    isChanged.set(true);
    existingPositions.forEach(
        (TrendingPosition postion) -> {
          Set<String> channels = TrendingBetsContext.getSelectionMappings().get(postion.getEvent());
          if (CollectionUtils.isEmpty(channels)) return;
          channels.remove(channelId);
          if (channels.isEmpty()) {
            TrendingBetsContext.cleanSelections(postion.getEvent(), betType);
          }
        });
  }

  public void updateTrendingBetsToContext() {

    TrendingBetsContext.getTrendingBets().put(channelId, buildTrendingBets());
  }

  public PersonalizedBetsDto buildTrendingBets() {
    return PersonalizedBetsDto.builder()
        .updatedAt(latestUpdate)
        .positions(positions)
        .fzYourTeamPositions(fzYourTeamPositions)
        .fzOtherTeamPositions(fzOtherTeamPositions)
        .isNewUser(isNewUser)
        .build();
  }

  public TrendingBetsDto buildLastMsgUpdatedAt() {
    return TrendingBetsDto.builder()
        .lastMsgUpdatedAt(latestUpdate)
        .positions(new HashSet<>())
        .build();
  }

  public void updateExistingPositions() {
    Optional<TrendingBetsDto> trendingBets =
        Optional.ofNullable(TrendingBetsContext.getTrendingBets().get(channelId));

    trendingBets.ifPresent(
        (TrendingBetsDto existingTrendingBets) -> {
          if (TrendingBetsUtil.isBefore(latestUpdate, existingTrendingBets.getUpdatedAt())) {
            log.warn(
                "Skipping payload:: received outdated data :: {} last update {}",
                channelId,
                latestUpdate);
            outDatedPayload = true;
          } else {
            this.existingPositions.addAll(existingTrendingBets.getPositions());
          }
        });
  }

  public void updatePostionsToAccaContext() {
    PopularAccaContext.addItemsToQueue(channelId, positions);
  }
}
