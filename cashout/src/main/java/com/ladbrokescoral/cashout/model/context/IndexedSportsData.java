package com.ladbrokescoral.cashout.model.context;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.ConfirmingResult;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Outcome;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part;
import com.ladbrokescoral.cashout.service.BetWithSelectionsModel;
import com.ladbrokescoral.cashout.service.BetWithSelectionsModel.SelectionDataLeg;
import com.ladbrokescoral.cashout.service.SelectionData;
import com.ladbrokescoral.cashout.service.SelectionDataPrice;
import com.ladbrokescoral.cashout.util.BetUtil;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import lombok.ToString;
import org.apache.commons.lang3.math.NumberUtils;

@ToString
public class IndexedSportsData {

  private final Map<BigInteger, SelectionData> indexBySelectionId;
  private final Map<BigInteger, Set<SelectionData>> indexByMarketId;
  private final Map<BigInteger, Set<SelectionData>> indexByEventId;

  private IndexedSportsData(
      Map<BigInteger, SelectionData> indexBySelectionId,
      Map<BigInteger, Set<SelectionData>> indexByMarketId,
      Map<BigInteger, Set<SelectionData>> indexByEventId) {
    this.indexBySelectionId = indexBySelectionId;
    this.indexByMarketId = indexByMarketId;
    this.indexByEventId = indexByEventId;
  }

  public List<SelectionData> getAllSelectionData() {
    return new ArrayList<>(indexBySelectionId.values());
  }

  public Set<BigInteger> getAllSelectionIds() {
    return indexBySelectionId.keySet();
  }

  public Set<BigInteger> getAllMarketIds() {
    return indexByMarketId.keySet();
  }

  public Set<BigInteger> getAllEventIds() {
    return indexByEventId.keySet();
  }

  public List<BetSummaryModel> getBetsWithSelection(BigInteger selectionId) {
    SelectionData selectionData = this.indexBySelectionId.get(selectionId);
    if (selectionData != null) {
      return selectionData.getBets();
    } else {
      return Collections.emptyList();
    }
  }

  public List<BetSummaryModel> getBetsWithMarketId(BigInteger marketId) {
    return this.indexByMarketId.getOrDefault(marketId, Collections.emptySet()).stream()
        .flatMap(s -> s.getBets().stream())
        .collect(Collectors.toList());
  }

  public List<BetSummaryModel> getBetsWithEventId(BigInteger eventId) {
    return this.indexByEventId.getOrDefault(eventId, Collections.emptySet()).stream()
        .flatMap(s -> s.getBets().stream())
        .collect(Collectors.toList());
  }

  public Optional<SelectionData> getSelectionDataBySelectionId(BigInteger selectionId) {
    return Optional.ofNullable(indexBySelectionId.get(selectionId));
  }

  public Set<SelectionData> getSelectionDataByMarketId(BigInteger marketId) {
    return indexByMarketId.getOrDefault(marketId, Collections.emptySet());
  }

  public Set<SelectionData> getSelectionDataByEventId(BigInteger eventId) {
    return indexByEventId.getOrDefault(eventId, Collections.emptySet());
  }

  public Set<SelectionData> findOtherSelectionsInBet(BetSummaryModel bet, BigInteger selectionId) {
    return bet.getLeg().stream()
        .flatMap(l -> l.getPart().stream())
        .map(p -> p.getOutcome().get(0).getId())
        .map(BigInteger::new)
        .filter(id -> !id.equals(selectionId))
        .map(this.indexBySelectionId::get)
        .collect(Collectors.toSet());
  }

  public static IndexedSportsData constructIndexedData(List<BetSummaryModel> bets) {
    Map<BigInteger, SelectionData> indexBySelectionId = new HashMap<>();
    Map<BigInteger, Set<SelectionData>> indexByMarketId = new HashMap<>();
    Map<BigInteger, Set<SelectionData>> indexByEventId = new HashMap<>();

    for (BetSummaryModel bet : bets) {
      for (Part part : partsInLeg(bet)) {
        Outcome outcome = part.getOutcome().get(0);
        BigInteger selectionId = new BigInteger(outcome.getId());
        BigInteger marketId = new BigInteger(outcome.getMarket().getId());
        BigInteger eventId = new BigInteger(outcome.getEvent().getId());

        indexBySelectionId.computeIfPresent(
            selectionId, (key, val) -> updateSelection(val, bet, part));

        indexBySelectionId.computeIfAbsent(
            selectionId,
            key -> {
              SelectionData selectionData =
                  updateSelection(new SelectionData(eventId, marketId, selectionId), bet, part);

              indexByEventId.putIfAbsent(eventId, new HashSet<>());
              indexByMarketId.putIfAbsent(marketId, new HashSet<>());
              indexByEventId.get(eventId).add(selectionData);
              indexByMarketId.get(marketId).add(selectionData);
              return selectionData;
            });
      }
    }

    return new IndexedSportsData(indexBySelectionId, indexByMarketId, indexByEventId);
  }

  private static List<Part> partsInLeg(BetSummaryModel bet) {
    return bet.getLeg().stream().flatMap(l -> l.getPart().stream()).collect(Collectors.toList());
  }

  private static SelectionData updateSelection(
      SelectionData selectionData, BetSummaryModel bet, Part part) {
    selectionData.getBets().add(bet);
    selectionData.getParts().add(part);
    boolean isCashoutAvailable = NumberUtils.isCreatable(bet.getCashoutValue());
    ConfirmingResult result = part.getOutcome().get(0).getResult();
    boolean isConfirmed = result != null && "Y".equals(result.getConfirmed());
    boolean isHandicapMarket = BetUtil.isBetOnHandicapMarket(bet, selectionData.getSelectionId());

    if (isHandicapMarket) {
      selectionData.setHandicapMarket(isHandicapMarket);
    }

    if (isConfirmed) {
      selectionData.setConfirmed(true);
    }

    // if cashout is available then all selection in bet must be active
    if (isCashoutAvailable) {
      selectionData.changeEventStatus(true);
      selectionData.changeMarketStatus(true);
      selectionData.changeSelectionStatus(true);
    }

    return selectionData;
  }

  public List<BetWithSelectionsModel> getBetWithSelectionModels(BigInteger selectionId) {
    List<BetWithSelectionsModel> result = new ArrayList<>();
    List<BetSummaryModel> betSummeryModels =
        getBetsWithSelection(selectionId).stream()
            .filter(
                bet ->
                    NumberUtils.isCreatable(bet.getCashoutValue())
                        || "CASHOUT_SELN_SUSPENDED".equals(bet.getCashoutValue())
                        || "CASHOUT_SELN_NO_CASHOUT".equals(BetUtil.getCashoutValueFromHRBet(bet)))
            .collect(Collectors.toList());

    for (BetSummaryModel betSummaryModel : betSummeryModels) {

      List<SelectionDataLeg> legs =
          betSummaryModel.getLeg().stream()
              .flatMap(l -> l.getPart().stream())
              .map(this::partToSelectionLeg)
              .collect(Collectors.toList());

      result.add(
          BetWithSelectionsModel.builder()
              .originalBet(betSummaryModel)
              .isBanachBet(BetUtil.isBanachBet(betSummaryModel))
              .legs(legs)
              .build());
    }
    return result;
  }

  private SelectionDataLeg partToSelectionLeg(Part p) {
    String priceTypeCode = p.getPrice().get(0).getPriceType().getCode();
    String id = p.getOutcome().get(0).getId();
    SelectionData selectionData = indexBySelectionId.get(new BigInteger(id));

    Supplier<Optional<SelectionDataPrice>> priceSupplier = Optional::empty;

    if ("L".equalsIgnoreCase(priceTypeCode)) {
      priceSupplier = selectionData::getLpPrice;
    } else if ("S".equalsIgnoreCase(priceTypeCode)) {
      priceSupplier = selectionData::getSpPrice;
    } else {
      priceSupplier =
          selectionData.getLpPrice().isPresent() ? selectionData::getLpPrice : priceSupplier;
    }

    return new SelectionDataLeg(selectionData, priceSupplier);
  }
}
