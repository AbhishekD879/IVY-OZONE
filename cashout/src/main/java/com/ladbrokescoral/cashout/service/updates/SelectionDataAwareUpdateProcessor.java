package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.converter.BetToCashoutOfferRequestConverter;
import com.ladbrokescoral.cashout.model.context.SelectionPrice;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.HasStatus;
import com.ladbrokescoral.cashout.model.safbaf.Market;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.repository.SelectionPriceRepository;
import com.ladbrokescoral.cashout.service.BetDetailMeta;
import com.ladbrokescoral.cashout.service.BetWithSelectionsModel;
import com.ladbrokescoral.cashout.service.BetWithSelectionsModel.SelectionDataLeg;
import com.ladbrokescoral.cashout.service.CashoutAvailability;
import com.ladbrokescoral.cashout.service.SelectionData;
import com.ladbrokescoral.cashout.service.updates.SafUpdateApplier.ChangeInfo;
import com.ladbrokescoral.cashout.util.BetUtil;
import com.ladbrokescoral.cashout.util.Message;
import com.newrelic.api.agent.NewRelic;
import io.netty.util.NettyRuntime;
import java.math.BigInteger;
import java.time.Duration;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Date;
import java.util.EnumSet;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Scheduler;
import reactor.core.scheduler.Schedulers;

public class SelectionDataAwareUpdateProcessor<T extends HasStatus> {

  private SafUpdateApplier<T> updateApplier;
  private UserUpdateTrigger userUpdateTrigger;
  private SelectionPriceRepository selectionPriceRepository;
  private BetToCashoutOfferRequestConverter converter;
  private Scheduler afterPriceUpdateExecutor;
  private CashoutService cashoutOfferService;
  private String[] twoUpMarkets;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private Message message;

  public SelectionDataAwareUpdateProcessor(
      SafUpdateApplier<T> updateApplier,
      UserUpdateTrigger userUpdateTrigger,
      SelectionPriceRepository selectionPriceRepository,
      BetToCashoutOfferRequestConverter converter,
      int cpuFactor,
      CashoutService cashoutOfferService,
      String[] twoUpMarkets) {
    this.updateApplier = updateApplier;
    this.userUpdateTrigger = userUpdateTrigger;
    this.selectionPriceRepository = selectionPriceRepository;
    this.converter = converter;
    this.afterPriceUpdateExecutor =
        Schedulers.newParallel(
            "Selection-Aware-Update-Parallel", (NettyRuntime.availableProcessors() * cpuFactor));
    this.cashoutOfferService = cashoutOfferService;
    this.twoUpMarkets = twoUpMarkets;
  }

  void sendBetUpdateIfNeeded(BetDetailMeta betDetailMeta) {
    if (betDetailMeta.hasBets()) {
      NewRelic.recordMetric(
          "Custom/UpdateTrigger/BetDetail/ConnectionAgeSeconds",
          betDetailMeta.getConnectionAgeInSeconds());
      NewRelic.incrementCounter(
          "Custom/UpdateTrigger/BetDetail/Reason/" + betDetailMeta.getReasonForUpdate());

      BetDetailRequestCtx betDetailrequestCtx =
          BetDetailRequestCtx.builder()
              .userId(betDetailMeta.getUsername())
              .timeToTokenExpirationLeft(betDetailMeta.getTokenExpiresIn())
              .request(
                  buildGetBetDetailRequest(betDetailMeta.getToken(), betDetailMeta.getBetIds()))
              .build();
      cashoutOfferService.getBetDetail(betDetailrequestCtx);
    }
  }

  protected static long connectionAgeInSeconds(UserRequestContextAccHistory ctx) {
    long connectionAge = new Date().getTime() - ctx.getConnectionDate().getTime();
    return Duration.ofMillis(connectionAge).getSeconds();
  }

  public static GetBetDetailRequest buildGetBetDetailRequest(String token, List<String> betId) {
    return GetBetDetailRequest.builder()
        .token(token)
        .returnFormattedHandicap("Y")
        .returnPartialCashoutDetails("Y")
        .betIds(betId)
        .build();
  }

  protected Mono<List<SelectionPrice>> updateSelectionsPrices(
      Set<SelectionData> selectionsToUpdate) {
    Map<String, List<SelectionData>> selectionsGroupedById =
        selectionsToUpdate.stream()
            .collect(Collectors.groupingBy(s -> String.valueOf(s.getSelectionId())));

    if (selectionsGroupedById.isEmpty()) {
      return Mono.empty();
    }
    return selectionPriceRepository
        .multiGet(selectionsGroupedById.keySet())
        .publishOn(afterPriceUpdateExecutor)
        .doOnNext(
            prices ->
                prices.stream()
                    .filter(Objects::nonNull)
                    .forEach(
                        p -> {
                          if (Objects.isNull(p.getOutcomeId())) {
                            ASYNC_LOGGER.warn("Price without outcomeId {}", p);
                          } else {
                            selectionsGroupedById
                                .getOrDefault(p.getOutcomeId(), Collections.emptyList())
                                .forEach(
                                    s ->
                                        s.changeLpPrice(
                                            Integer.parseInt(p.getPriceNum()),
                                            Integer.parseInt(p.getPriceDen())));
                          }
                        }));
  }

  // update -> event/market/selection update
  protected void processUpdateWithSelectionDataInContext(
      UserRequestContextAccHistory context, T update, Set<SelectionData> selections) {
    Set<SelectionData> selectionsWithoutLpPrices =
        selections.stream()
            .flatMap(
                sel ->
                    context.getIndexedData().getBetWithSelectionModels(sel.getSelectionId())
                        .stream())
            .flatMap(bet -> bet.getLegs().stream())
            .map(SelectionDataLeg::getSelectionData)
            .filter(selData -> !currentUpdateWillChangePrice(selData, update))
            .filter(selData -> !selData.getLpPrice().isPresent())
            .collect(Collectors.toSet());
    message = new Message();
    message.setMessage(twoUpMarkets.toString());
    ASYNC_LOGGER.info(
        "Market Update :: {} TwoUpMarkets are :: {}", update instanceof Market, message);

    updateSelectionsPrices(selectionsWithoutLpPrices)
        .doFinally(
            sig ->
                selections.forEach(
                    selData -> {
                      CashoutChange cashoutChange =
                          CashoutChangeImpl.applyUpdateAndGetChange(
                              context,
                              selData.getSelectionId(),
                              () -> updateApplier.applyChange(selData, update),
                              update instanceof Market ? Arrays.asList(twoUpMarkets) : null);

                      if (updateApplier.needToCallServices(selData, update)) {
                        doGetBetDetailForBetsThatNeedIt(
                            context, cashoutChange, update, selData.getSelectionId());
                      } else {
                        ASYNC_LOGGER.info("Ignore to call openbet for {}", update);
                      }
                    }))
        .subscribe();
  }

  protected void incrementCountOfBetIdsForAvailabiityStatus(
      int count, CashoutAvailability cashoutAvailability, String updateType) {

    String metricName =
        String.format(
            "Custom/BetDetailTrigger/CashoutAvail/%s/%s", cashoutAvailability, updateType);
    NewRelic.incrementCounter(metricName, count);
  }

  protected boolean currentUpdateWillChangePrice(SelectionData selData, HasStatus update) {
    if (!(update instanceof Selection)) {
      return false;
    } else {
      Selection selUpdate = (Selection) update;
      return selUpdate.getSelectionKey() == selData.getSelectionId()
          && selUpdate.getLpPrice().isPresent();
    }
  }

  protected void doGetBetDetailForBetsThatNeedIt(
      UserRequestContextAccHistory context,
      CashoutChange cashoutChange,
      T update,
      BigInteger selectionId) {
    String reason = update.reasonForUpdate();

    EnumSet<ChangeInfo> changeSet = cashoutChange.getChangeSet();
    boolean isLpPriceChanged = changeSet.contains(ChangeInfo.LP_PRICE_CHANGED);

    Set<BetSummaryModel> bets =
        Stream.of(
                cashoutChange.betsAfterChange(CashoutAvailability.YES),
                cashoutChange.betsAfterChange(CashoutAvailability.UNKNOWN),
                cashoutChange.betsThatRemainedStatus(CashoutAvailability.UNKNOWN_UNCOMPETITIVE))
            .flatMap(Collection::stream)
            .filter(b -> !b.isBanachBet())
            .map(BetWithSelectionsModel::getOriginalBet)
            // we should regular cashoutUpdate only on price change! THAT'S ALL
            .filter(bet -> updateApplier.canSendCashoutUpdate(cashoutChange, selectionId, bet))
            .collect(Collectors.toSet());

    cashoutOfferService.prepareCashoutReq(bets, false);

    if (isLpPriceChanged) {
      Set<String> betIdsWithUnknownCashoutAvailability =
          cashoutChange.betsAfterChange(CashoutAvailability.UNKNOWN).stream()
              .filter(BetWithSelectionsModel::isBanachBet)
              .map(BetWithSelectionsModel::getOriginalBet)
              .map(BetSummaryModel::getId)
              .collect(Collectors.toSet());

      incrementCountOfBetIdsForAvailabiityStatus(
          betIdsWithUnknownCashoutAvailability.size(),
          CashoutAvailability.UNKNOWN,
          "BanachPriceChange");

      Set<String> betIdsThatBecameUnknownPrice =
          cashoutChange.betsThatChangedTo(CashoutAvailability.UNKNOWN_UNCOMPETITIVE).stream()
              .filter(b -> !b.isBanachBet())
              .map(BetWithSelectionsModel::getOriginalBet)
              .filter(bet -> BetUtil.isBetOnLPPrice(bet, selectionId))
              .map(BetSummaryModel::getId)
              .collect(Collectors.toSet());

      incrementCountOfBetIdsForAvailabiityStatus(
          betIdsThatBecameUnknownPrice.size(),
          CashoutAvailability.UNKNOWN_UNCOMPETITIVE,
          "LpPriceChange");

      betIdsWithUnknownCashoutAvailability.addAll(betIdsThatBecameUnknownPrice);

      getBetDetail(context, update, betIdsWithUnknownCashoutAvailability);
    }

    Set<String> betIdsForGetBetDetail = new HashSet<>();

    if (updateApplier.couldChangeCashoutAvailability(context, update)) {
      List<BetWithSelectionsModel> unknownBets =
          cashoutChange.betsAfterChange(CashoutAvailability.UNKNOWN);
      List<BetWithSelectionsModel> betsRemainedAvailable =
          cashoutChange.betsThatRemainedStatus(CashoutAvailability.YES);
      List<BetWithSelectionsModel> unknownUncompetitiveBets =
          cashoutChange.betsAfterChange(CashoutAvailability.UNKNOWN_UNCOMPETITIVE);

      betIdsForGetBetDetail.addAll(
          Stream.of(unknownBets, betsRemainedAvailable, unknownUncompetitiveBets)
              .flatMap(Collection::stream)
              .map(BetWithSelectionsModel::getOriginalBet)
              .map(BetSummaryModel::getId)
              .collect(Collectors.toSet()));

      incrementCountOfBetIdsForAvailabiityStatus(
          unknownBets.size(), CashoutAvailability.UNKNOWN, reason);
      incrementCountOfBetIdsForAvailabiityStatus(
          betsRemainedAvailable.size(), CashoutAvailability.YES, reason);
      incrementCountOfBetIdsForAvailabiityStatus(
          unknownUncompetitiveBets.size(), CashoutAvailability.UNKNOWN_UNCOMPETITIVE, reason);
    } else {
      Set<String> betsBecameUnknown =
          cashoutChange.betsThatChangedTo(CashoutAvailability.UNKNOWN).stream()
              .map(BetWithSelectionsModel::getOriginalBet)
              .map(BetSummaryModel::getId)
              .collect(Collectors.toSet());
      incrementCountOfBetIdsForAvailabiityStatus(
          betsBecameUnknown.size(), CashoutAvailability.UNKNOWN, "ChangedTo/" + reason);
      betIdsForGetBetDetail.addAll(betsBecameUnknown);
    }

    Set<BetSummaryModel> betsThatBecameActive =
        cashoutChange.betsThatChangedTo(CashoutAvailability.YES).stream()
            .map(BetWithSelectionsModel::getOriginalBet)
            .collect(Collectors.toSet());

    Set<String> betIdsConfirmed =
        cashoutChange.betsThatChangedTo(CashoutAvailability.NO_CONFIRMED).stream()
            .map(l -> l.getOriginalBet().getId())
            .collect(Collectors.toSet());

    if (!betIdsConfirmed.isEmpty()) {
      userUpdateTrigger.triggerBetSettled(
          UserUpdateTriggerDto.builder().betIds(betIdsConfirmed).token(context.getToken()).build());
    }

    cashoutOfferService.prepareCashoutReq(betsThatBecameActive, true);

    Set<String> betIdsBecomeSuspended =
        cashoutChange.betsThatChangedTo(CashoutAvailability.NO).stream()
            .map(BetWithSelectionsModel::getOriginalBet)
            .map(BetSummaryModel::getId)
            .collect(Collectors.toSet());

    if (!betIdsBecomeSuspended.isEmpty()) {
      incrementCountOfBetIdsSuspended(update, betIdsBecomeSuspended.size());
      userUpdateTrigger.triggerCashoutSuspension(
          UserUpdateTriggerDto.builder()
              .token(context.getToken())
              .betIds(betIdsBecomeSuspended)
              .build());
    }

    getBetDetail(context, update, betIdsForGetBetDetail);
  }

  public void getBetDetail(UserRequestContextAccHistory context, T update, Set<String> betIds) {
    if (!betIds.isEmpty()) {
      List<List<String>> betIdSubList = cashoutOfferService.betIdSubList(betIds);
      betIdSubList.forEach(
          betId ->
              sendBetUpdateIfNeeded(
                  BetDetailMeta.builder()
                      .token(context.getToken())
                      .username(context.getUsername())
                      .tokenExpiresIn(context.getTokenExpiresIn())
                      .betIds(betId)
                      .connectionAgeInSeconds(connectionAgeInSeconds(context))
                      .reasonForUpdate(update.reasonForUpdate())
                      .build()));
    }
  }

  // for testing purposes
  public void setAfterPriceUpdateExecutor(Scheduler afterPriceUpdateExecutor) {
    this.afterPriceUpdateExecutor = afterPriceUpdateExecutor;
  }

  void incrementCountOfBetIdsSuspended(HasStatus update, int count) {
    NewRelic.incrementCounter(
        String.format("Custom/SuspensionTrigger/%s", update.getClass().getSimpleName()), count);
  }

  interface CashoutChange {

    List<BetWithSelectionsModel> betsBeforeChange(CashoutAvailability availability);

    List<BetWithSelectionsModel> betsAfterChange(CashoutAvailability availability);

    List<BetWithSelectionsModel> betsThatRemainedStatus(CashoutAvailability availability);

    List<BetWithSelectionsModel> betsThatChangedTo(CashoutAvailability availability);

    EnumSet<ChangeInfo> getChangeSet();
  }

  static class CashoutChangeImpl implements CashoutChange {

    private final EnumSet<ChangeInfo> changeSet;

    private final Map<CashoutAvailability, List<BetWithSelectionsModel>>
        cashoutAvailabilityBeforeChangeApplied;
    private final Map<CashoutAvailability, List<BetWithSelectionsModel>> cashoutAvailabilityForBets;

    private CashoutChangeImpl(
        EnumSet<ChangeInfo> changeSet,
        Map<CashoutAvailability, List<BetWithSelectionsModel>>
            cashoutAvailabilityBeforeChangeApplied,
        Map<CashoutAvailability, List<BetWithSelectionsModel>> cashoutAvailabilityForBets) {
      this.changeSet = changeSet;
      this.cashoutAvailabilityBeforeChangeApplied = cashoutAvailabilityBeforeChangeApplied;
      this.cashoutAvailabilityForBets = cashoutAvailabilityForBets;
    }

    public static CashoutChange applyUpdateAndGetChange(
        UserRequestContextAccHistory context,
        BigInteger bigInteger,
        Supplier<EnumSet<ChangeInfo>> changeProcess,
        List<String> twoUpMarkets) {

      Map<CashoutAvailability, List<BetWithSelectionsModel>>
          cashoutAvailabilityBeforeChangeApplied =
              context.getIndexedData().getBetWithSelectionModels(bigInteger).stream()
                  .filter(bet -> !context.isBetSettled(bet))
                  .collect(
                      Collectors.groupingBy(
                          bet ->
                              CashoutAvailability.calculateCashoutAvailability(bet, twoUpMarkets)));

      ASYNC_LOGGER.info(
          "[{}] Before change Calculated availability: {}",
          context.getToken(),
          cashoutAvailabilityBeforeChangeApplied);

      EnumSet<ChangeInfo> changeSet = changeProcess.get();

      Map<CashoutAvailability, List<BetWithSelectionsModel>> cashoutAvailabilityForBets =
          context.getIndexedData().getBetWithSelectionModels(bigInteger).stream()
              .filter(bet -> !context.isBetSettled(bet))
              .collect(
                  Collectors.groupingBy(
                      bet -> CashoutAvailability.calculateCashoutAvailability(bet, twoUpMarkets)));

      ASYNC_LOGGER.info(
          "[{}] ChangeSet: {}. Calculated availability: {}",
          context.getToken(),
          changeSet,
          cashoutAvailabilityForBets);

      return new CashoutChangeImpl(
          changeSet, cashoutAvailabilityBeforeChangeApplied, cashoutAvailabilityForBets);
    }

    @Override
    public List<BetWithSelectionsModel> betsBeforeChange(CashoutAvailability availability) {
      return cashoutAvailabilityBeforeChangeApplied.getOrDefault(
          availability, Collections.emptyList());
    }

    @Override
    public List<BetWithSelectionsModel> betsAfterChange(CashoutAvailability availability) {
      return cashoutAvailabilityForBets.getOrDefault(availability, Collections.emptyList());
    }

    @Override
    public List<BetWithSelectionsModel> betsThatRemainedStatus(CashoutAvailability availability) {
      List<BetWithSelectionsModel> betsWithThisAvailabilityBeforeChange =
          cashoutAvailabilityBeforeChangeApplied.getOrDefault(
              availability, Collections.emptyList());
      return cashoutAvailabilityForBets.getOrDefault(availability, Collections.emptyList()).stream()
          .filter(betsWithThisAvailabilityBeforeChange::contains)
          .collect(Collectors.toList());
    }

    @Override
    public List<BetWithSelectionsModel> betsThatChangedTo(CashoutAvailability availability) {
      return betsAfterChange(availability).stream()
          .filter(b -> !betsBeforeChange(availability).contains(b))
          .collect(Collectors.toList());
    }

    @Override
    public EnumSet<ChangeInfo> getChangeSet() {
      return changeSet;
    }
  }
}
