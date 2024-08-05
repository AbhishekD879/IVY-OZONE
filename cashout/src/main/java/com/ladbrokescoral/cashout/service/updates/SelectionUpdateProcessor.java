package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.DeadHeat;
import com.ladbrokescoral.cashout.model.safbaf.Price;
import com.ladbrokescoral.cashout.model.safbaf.Rule4;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.payout.PayoutUpdatesPublisher;
import com.newrelic.api.agent.NewRelic;
import java.math.BigInteger;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.regex.Pattern;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;

@Service
public class SelectionUpdateProcessor extends AbstractUpdateProcessor<Selection>
    implements UpdateProcessor<Selection> {

  private static final int SECOND = 2;
  private static final Pattern splitPattern = Pattern.compile(":");
  private static final String KAFKA_MESSAGES_SELECTION = "/Kafka/Messages/Selection";
  private PayoutUpdatesPublisher payoutUpdatesPublisher;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private TwoUpUpdatesPublisher twoUpUpdatesPublisher;

  public SelectionUpdateProcessor(
      SelectionDataAwareUpdateProcessor<Selection> processor,
      PayoutUpdatesPublisher payoutUpdatesPublisher,
      TwoUpUpdatesPublisher twoUpUpdatesPublisher) {
    super(processor);
    this.payoutUpdatesPublisher = payoutUpdatesPublisher;
    this.twoUpUpdatesPublisher = twoUpUpdatesPublisher;
  }

  /*-
   * Call BPP betDetail in case update selection status and settled fields related to bet
   * Call Cashout V4 in case price change
   *
   * @param context         - User related data
   * @param selectionUpdate - kafka Saf selection update
   */
  @Override
  public void process(UserRequestContextAccHistory context, Selection selectionUpdate) {
    Optional<Rule4> rule4 = selectionUpdate.getRule4();
    if (Objects.nonNull(selectionUpdate.getSelectionKey())) {
      NewRelic.incrementCounter(KAFKA_MESSAGES_SELECTION);
      if (canProcess(selectionUpdate)) {
        ASYNC_LOGGER.debug("process - {}, {}", context.getUsername(), selectionUpdate);
        potentialReturnsServiceCall(context, selectionUpdate);
        doProcess(context, selectionUpdate);
      } else {
        ASYNC_LOGGER.debug("Ignored to process - {}, {}", context.getUsername(), selectionUpdate);
      }
    } else if (rule4.isPresent()) {
      setRule4DeductionFactor(context, selectionUpdate, rule4.get());
    }
  }

  private void setRule4DeductionFactor(
      UserRequestContextAccHistory context, Selection selectionUpdate, Rule4 rule4) {
    List<BetSummaryModel> betSummaryModels =
        context
            .getIndexedData()
            .getBetsWithMarketId(getMarketkey(selectionUpdate.getMeta().getParents()));
    payoutUpdatesPublisher.setRule4DeductionFactor(
        getMarketkey(selectionUpdate.getMeta().getParents()),
        rule4.getDeduction(),
        betSummaryModels);
  }

  private void doProcess(UserRequestContextAccHistory context, Selection selectionUpdate) {
    Optional.ofNullable(selectionUpdate.getSelectionKey())
        .flatMap(selId -> context.getIndexedData().getSelectionDataBySelectionId(selId))
        .ifPresent(
            selectionData ->
                selectionDataAwareUpdateProcessor.processUpdateWithSelectionDataInContext(
                    context, selectionUpdate, Collections.singleton(selectionData)));
  }

  private void potentialReturnsServiceCall(
      UserRequestContextAccHistory context, Selection selectionUpdate) {
    List<BetSummaryModel> betSummaryModels =
        context.getIndexedData().getBetsWithSelection(selectionUpdate.getSelectionKey());
    if (selectionUpdate.getResultCode().isPresent()) {
      payoutUpdatesPublisher.invokePayoutRequest(
          context.getToken(), selectionUpdate, betSummaryModels);
      twoUpUpdatesPublisher.publishTwoUpUpdates(
          context.getToken(), selectionUpdate, betSummaryModels);
    }
    Optional<Price> spPrice = selectionUpdate.getSpPrice();
    if (spPrice.isPresent()) {
      payoutUpdatesPublisher.setPrices(
          selectionUpdate.getSelectionKey(),
          spPrice.get().getNumPrice(),
          spPrice.get().getDenPrice(),
          betSummaryModels);
    }
    Optional<DeadHeat> deadheat = selectionUpdate.getDeadHeat();
    if (deadheat.isPresent()) {
      payoutUpdatesPublisher.setDeductionPrices(
          selectionUpdate.getSelectionKey(),
          deadheat.get().getWinNum(),
          deadheat.get().getWinDen(),
          betSummaryModels);
    }
  }

  private boolean canProcess(Selection selectionUpdate) {
    return !selectionUpdate.settledChanged();
  }

  private BigInteger getMarketkey(String msg) {
    String[] split = splitPattern.split(msg);
    return new BigInteger(split[split.length - 1].substring(SECOND));
  }
}
