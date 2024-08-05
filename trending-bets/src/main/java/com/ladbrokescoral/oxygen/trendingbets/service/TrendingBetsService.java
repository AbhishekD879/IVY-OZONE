package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetSession;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularBets;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingBets;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.model.MessageContent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.TrendingBetsSiteServImpl;
import com.ladbrokescoral.oxygen.trendingbets.util.TrendingBetsUtil;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Sinks;

@Service
@Slf4j
public class TrendingBetsService extends PopularBetsService {

  private String preMatchEventType;

  private String allPayloadType;

  @Autowired
  public TrendingBetsService(
      LiveUpdatesService liveUpdatesService,
      TrendingBetsSiteServImpl siteServeService,
      @Value("${popularbets.filter.market.drilldownTagNames}")
          String[] filterMarketDrilldownTagNames,
      @Value("${popularbets.filter.event.drilldownTagNames}") String[] filterEventDrilldownTagNames,
      @Value("${popularbets.prematch.eventType}") String preMatchEventType,
      @Value("${popularbets.all.payloadType}") String allPayloadType) {
    super(
        liveUpdatesService,
        siteServeService,
        filterMarketDrilldownTagNames,
        filterEventDrilldownTagNames);
    this.preMatchEventType = preMatchEventType;
    this.allPayloadType = allPayloadType;
  }

  private final Sinks.EmitFailureHandler emitFailureHandler =
      (signalType, emitResult) -> emitResult.equals(Sinks.EmitResult.FAIL_NON_SERIALIZED);

  /**
   * Processes the TrendingBets if received frontend matches with configured frontend and not
   * outdated data.
   *
   * @param trendingBets
   * @return
   */
  public Mono<TrendingBetSession> processTrendingBets(TrendingBets trendingBets) {
    if (!frontend.equalsIgnoreCase(trendingBets.frontend())
        || !isPreMatchDefaultPopularBets(trendingBets)) {
      log.debug(
          "Skipping the payload:: frontend configured {}, received {}",
          frontend,
          trendingBets.frontend());
      return Mono.empty();
    }
    TrendingBetSession trendingBetsession =
        new TrendingBetSession(
            liveUpdatesService,
            getChannelId(trendingBets),
            trendingBets.lastUpdate(),
            getBetType());

    trendingBetsession.updateExistingPositions();
    if (trendingBetsession.isOutDatedPayload()) return Mono.empty();

    return siteServeService
        .getEventToOutcomeForOutcome(trendingBets.events())
        .map(this::enhanceTrendingBets)
        .map(events -> updateSessionWithNewSelectionsAndPostions(trendingBetsession, events))
        .doOnNext(TrendingBetSession::updateRanksOfPositions)
        .doOnNext(TrendingBetSession::updatePostionsToAccaContext)
        .doOnNext(TrendingBetSession::updateSelectionChannels)
        .doOnNext(this::notifyIfChanged)
        .doOnNext(TrendingBetSession::updateTrendingBetsToContext);
  }

  private boolean isPreMatchDefaultPopularBets(TrendingBets trendingBets) {
    if ((!StringUtils.hasText(trendingBets.eventType())
            || trendingBets.eventType().equalsIgnoreCase(preMatchEventType))
        && (!StringUtils.hasText(trendingBets.payloadType())
            || trendingBets.payloadType().equalsIgnoreCase(allPayloadType))) {
      return true;
    } else {
      log.info(
          "Skipping payload :: eventtype {} :: payloadtype : {}",
          trendingBets.eventType(),
          trendingBets.payloadType());
      return false;
    }
  }

  /**
   * Processes the TrendingBets if received frontend matches with configured frontend and not
   * outdated data.
   *
   * @param trendingBets
   * @return
   */
  @NotNull
  private static String getChannelId(TrendingBets trendingBets) {
    return TrendingBetsUtil.prepareChannelId(
        trendingBets.sport(), trendingBets.backedWithIn(), trendingBets.eventStartIn());
  }

  /**
   * Notifies to the clients of specific channel if any change is detected in trending bets
   *
   * @param session
   */
  private void notifyIfChanged(TrendingBetSession session) {

    Optional.ofNullable(ChannelHandlersContext.getChannels().get(session.getChannelId()))
        .ifPresent(
            (Sinks.Many<Message<String>> channel) -> {
              if (session.getIsChanged().get()) {
                log.debug("Notifying Changes for :: {}", session.getChannelId());
                channel.emitNext(
                    MessageContent.withPayload(session.getChannelId(), session.buildTrendingBets()),
                    emitFailureHandler);
              } else {
                channel.emitNext(
                    MessageContent.withPayload(
                        session.getChannelId(), session.buildLastMsgUpdatedAt()),
                    emitFailureHandler);
              }
            });
  }

  /**
   * Populates TrendingPositions and updates previous rank for each trending position. Events will
   * be added to new selections list if it is newly added to trending bets.
   *
   * @param session
   * @param items
   * @return
   */
  private TrendingBetSession updateSessionWithNewSelectionsAndPostions(
      TrendingBetSession session, List<TrendingItem> items) {
    items.forEach(
        (TrendingItem item) -> {
          TrendingPosition position = populateAndAddTrendingPosition(item, session);
          if (position.getPreviousRank() == 0) {
            session.getIsChanged().set(true);
            addToNewSelections(session, position);
          }
        });
    return session;
  }

  private static void addToPostions(TrendingBetSession session, TrendingPosition position) {
    session.getPositions().add(position);
  }

  private static void addToNewSelections(TrendingBetSession session, TrendingPosition position) {
    session.getNewSelections().add(position.getEvent());
  }

  /**
   * Populates TrendingPosition and updates previous rank if it is already exist in the channel.
   *
   * @param item
   * @param session
   * @return TrendingPosition
   */
  private TrendingPosition populateAndAddTrendingPosition(
      TrendingItem item, TrendingBetSession session) {
    TrendingPosition position = populateTrendingPosition(item);
    updatePrevRankAndRemoveExsistingPostions(session, position);
    addToPostions(session, position);
    return position;
  }

  private static void updatePrevRankAndRemoveExsistingPostions(
      TrendingBetSession session, TrendingPosition position) {
    Optional<TrendingPosition> existingPosition =
        session.getExistingPositions().stream()
            .filter(ep -> ep.getEvent().equals(position.getEvent()))
            .findFirst();
    existingPosition.ifPresent(
        (TrendingPosition ep) -> {
          position.setPreviousRank(ep.getRank());
          session.getExistingPositions().remove(ep);
        });
  }

  protected PopularBets getBetType() {
    return PopularBets.TRENDING_BETS;
  }
}
