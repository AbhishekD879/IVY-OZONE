package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.util.BetUtils;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.BetDelay;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.BetPlacement;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespStatus;
import io.vavr.collection.List;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public class MultiPlaceBetResponseAdapter implements PlaceBetResponseAdapter {

  private static final Integer DEFAULT_ASK_DELAY = 3;

  private final RespBetPlace respBetPlace;

  @Override
  public boolean allFinished() {
    return !isOverask() && !isBetInRun();
  }

  @Override
  public boolean isOverask() {
    return respBetPlace.getBetPlacement().stream()
        .map(BetPlacement::getBet)
        .anyMatch(bet -> bet.getStatus() == RespStatus.P);
  }

  private List<Bet> getPendingBets() {
    return List.ofAll(respBetPlace.getBetPlacement())
        .map(BetPlacement::getBet)
        .filter(bet -> bet.getStatus() == RespStatus.P);
  }

  @Override
  public boolean isBetInRun() {
    return !respBetPlace.getBetDelay().isEmpty();
  }

  @Override
  public Object getResponse() {
    return respBetPlace;
  }

  @Override
  public String getConfirmationExpectedAt() {
    return String.valueOf(
        respBetPlace.getBetDelay().stream()
            .map(BetDelay::getDelay)
            .mapToInt(Integer::valueOf)
            .max()
            .orElse(DEFAULT_ASK_DELAY));
  }

  @Override
  public String getProvider() {
    return isBetInRun() ? BetUtils.OPEN_BET_BIR_PROVIDER : BetUtils.OPEN_BET_OVERASK_PROVIDER;
  }

  @Override
  public List<Long> getIds() {
    return getBetsToRead().map(BetRef::getId).map(Long::valueOf);
  }

  @Override
  public List<BetRef> getBetsToRead() {
    if (isOverask()) {
      return getPendingBets()
          .map(bet -> new BetRef(bet.getBetId().getContent(), BetUtils.OPEN_BET_OVERASK_PROVIDER));
    } else if (isBetInRun()) {
      return List.ofAll(respBetPlace.getBetDelay())
          .map(bet -> new BetRef(bet.getBirBetId(), getProvider()));
    } else {
      return List.empty();
    }
  }
}
