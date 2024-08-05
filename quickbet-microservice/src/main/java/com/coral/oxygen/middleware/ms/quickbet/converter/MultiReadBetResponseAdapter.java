package com.coral.oxygen.middleware.ms.quickbet.converter;

import static com.coral.oxygen.middleware.ms.quickbet.util.BettingApiBetUtils.isCancelled;
import static com.coral.oxygen.middleware.ms.quickbet.util.BettingApiBetUtils.isConfirmed;

import com.coral.oxygen.middleware.ms.quickbet.util.BettingApiBetUtils;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import io.vavr.collection.List;
import java.util.Objects;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public class MultiReadBetResponseAdapter implements PlaceBetResponseAdapter {

  private static final Integer DEFAULT_ASK_DELAY = 3;

  private final BetsResponse respBetPlace;

  @Override
  public boolean allFinished() {
    return respBetPlace.getBet().stream().allMatch(bet -> isConfirmed(bet) || isCancelled(bet));
  }

  @Override
  public boolean isOverask() {
    return respBetPlace.getBet().stream().anyMatch(BettingApiBetUtils::isBetOverask);
  }

  @Override
  public boolean isBetInRun() {
    return respBetPlace.getBet().stream().anyMatch(BettingApiBetUtils::isBetInRun);
  }

  @Override
  public Object getResponse() {
    return respBetPlace;
  }

  @Override
  public String getConfirmationExpectedAt() {
    return String.valueOf(
        List.ofAll(respBetPlace.getBet())
            .map(Bet::getConfirmationExpectedAt)
            .filter(Objects::nonNull)
            .map(Integer::parseInt)
            .max()
            .getOrElse(DEFAULT_ASK_DELAY));
  }

  @Override
  public String getProvider() {
    return isBetInRun() ? BettingApiBetUtils.OPEN_BET_BIR_PROVIDER : "Other";
  }

  @Override
  public List<Long> getIds() {
    return List.ofAll(respBetPlace.getBet()).map(Bet::getId);
  }

  @Override
  public List<BetRef> getBetsToRead() {
    return List.ofAll(respBetPlace.getBet())
        .map(bet -> new BetRef(bet.getId().toString(), bet.getProvider()));
  }
}
