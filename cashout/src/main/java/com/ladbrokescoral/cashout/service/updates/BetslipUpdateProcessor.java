package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Bet;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Bets;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip;
import com.newrelic.api.agent.NewRelic;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class BetslipUpdateProcessor implements UpdateProcessor<Betslip> {
  private static final String KAFKA_MESSAGES_BETSLIP = "/Kafka/Messages/Betslip";
  private final UserUpdateTrigger userUpdateTrigger;

  public BetslipUpdateProcessor(UserUpdateTrigger userUpdateTrigger) {
    this.userUpdateTrigger = userUpdateTrigger;
  }

  /*-
   * Process betslip updates
   * @param context - User related data
   * @param betslip - kafka Betslip update
   */
  public void process(UserRequestContextAccHistory context, Betslip betslip) {
    NewRelic.incrementCounter(KAFKA_MESSAGES_BETSLIP);
    if (betslip == null) {
      return;
    }

    if (Boolean.TRUE.equals(betslip.getIsSettled())) {
      doWithBetsInBetslipUpdates(
          betslip,
          bets -> {
            Set<String> settledBetIds =
                bets.stream().map(Bet::getBetKey).collect(Collectors.toSet());
            userUpdateTrigger.triggerBetSettled(
                UserUpdateTriggerDto.builder()
                    .betIds(settledBetIds)
                    .token(context.getToken())
                    .build());
            context.addSettledBets(settledBetIds);
          });
    } else {
      doWithBetsInBetslipUpdates(
          betslip,
          bets ->
              bets.stream()
                  .filter(b -> Objects.nonNull(b.getStake()))
                  .forEach(
                      bet ->
                          context.getUserBets().stream()
                              .filter(b -> b.getId().equals(bet.getBetKey()))
                              .filter(b -> Objects.nonNull(b.getStake()))
                              .findAny()
                              .ifPresent(
                                  (BetSummaryModel b) -> {
                                    b.getStake().setValue(bet.getStake());
                                    b.getStake()
                                        .setStakePerLine(String.valueOf(bet.getStakePerLine()));
                                  })));
    }
  }

  public void doWithBetsInBetslipUpdates(Betslip betslip, Consumer<List<Bet>> betListConsumer) {
    betListConsumer.accept(
        Optional.of(betslip)
            .map(Betslip::getBets)
            .map(Bets::getBet)
            .orElse(Collections.emptyList()));
  }
}
