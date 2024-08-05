package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
/** Created by azayats on 05.12.16. */
public class SimpleOutcomeMapper implements OutcomeMapper {

  @Override
  public OutputOutcome map(Event event, Market market, Outcome outcome) {
    OutputOutcome output = new OutputOutcome();
    output.setId(outcome.getId());
    output.setOutcomeMeaningMajorCode(outcome.getOutcomeMeaningMajorCode());
    output.setOutcomeMeaningMinorCode(outcome.getOutcomeMeaningMinorCode());
    output.setOutcomeMeaningScores(outcome.getOutcomeMeaningScores());
    output.setRunnerNumber(outcome.getRunnerNumber());
    output.setResulted(outcome.getIsResulted());
    output.setOutcomeStatusCode(outcome.getOutcomeStatusCode());
    output.setLiveServChannels(outcome.getLiveServChannels());
    output.setDisplayOrder(outcome.getDisplayOrder());
    output.setHasPriceStream(outcome.isHasPriceStream());
    output.setPrices(
        outcome.getPrices().stream()
            .filter(Objects::nonNull)
            .filter(this::filterPrices)
            .map(this::mapPrice)
            .collect(Collectors.toList()));

    Supplier<String> nameSupplier =
        () -> {
          if (!outcome.getPrices().isEmpty()
              && outcome.getPrices().get(0).getHandicapValueDec() != null) {
            String handicapValue =
                outcome.getPrices().get(0).getHandicapValueDec().replace(",", "");
            if (!handicapValue.isEmpty()
                && !handicapValue.startsWith("-")
                && !handicapValue.startsWith("0.00")) {
              handicapValue = "+" + handicapValue;
            }
            return String.format("%s (%s)", outcome.getName(), handicapValue);
          }
          return outcome.getName();
        };
    output.setName(nameSupplier.get());
    if (Objects.nonNull(outcome.getExtIds())) {
      List<String> extId = Arrays.asList(outcome.getExtIds().split(","));
      output.setBwinId(extId.get(1));
    }
    return output;
  }

  protected boolean filterPrices(Price price) {
    return Boolean.TRUE.equals(price.getIsActive());
  }

  protected OutputPrice mapPrice(Price price) {
    OutputPrice op = new OutputPrice();
    op.setId(price.getId());
    op.setPriceType(price.getPriceType());
    op.setPriceNum(price.getPriceNum());
    op.setPriceDen(price.getPriceDen());
    op.setPriceDec(price.getPriceDec());
    op.setPriceStreamType(price.getPriceStreamType());
    op.setPriceAmerican(price.getPriceAmerican());
    op.setHandicapValueDec(
        price.getHandicapValueDec() != null
            ? price.getHandicapValueDec().replace(",", "")
            : price.getHandicapValueDec());
    op.setRawHandicapValue(price.getRawHandicapValue());

    return op;
  }
}
