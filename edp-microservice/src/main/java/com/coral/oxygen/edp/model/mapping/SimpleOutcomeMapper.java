package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.coral.oxygen.edp.model.output.OutputPrice;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import java.util.ArrayList;
import java.util.Objects;
import java.util.function.Supplier;
import java.util.stream.Collectors;

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
    output.setIsResulted(outcome.getIsResulted());
    output.setOutcomeStatusCode(outcome.getOutcomeStatusCode());
    output.setLiveServChannels(outcome.getLiveServChannels());
    output.setDisplayOrder(outcome.getDisplayOrder());
    output.setHasPriceStream(outcome.isHasPriceStream());

    output.setPrices(
        outcome.getPrices().stream() //
            .filter(Objects::nonNull) //
            .filter(this::filterPrices) //
            .map(this::mapPrice) //
            .collect(Collectors.toCollection(ArrayList::new)));

    Supplier<String> nameSupplier =
        () -> {
          if (!outcome.getPrices().isEmpty()
              && outcome.getPrices().get(0).getHandicapValueDec() != null) {
            String handicapValue =
                outcome.getPrices().get(0).getHandicapValueDec().replace(",", "");
            String handicapValueWithSign =
                Math.signum(Double.valueOf(handicapValue)) > 0
                    ? "+" + handicapValue
                    : handicapValue;
            return outcome.getName() + " (" + handicapValueWithSign + ")";
          }
          return outcome.getName();
        };
    output.setName(nameSupplier.get());

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
    op.setHandicapValueDec(
        price.getHandicapValueDec() != null
            ? price.getHandicapValueDec().replace(",", "")
            : price.getHandicapValueDec());
    op.setRawHandicapValue(price.getRawHandicapValue());

    op.setPriceStreamType(price.getPriceStreamType());

    return op;
  }
}
