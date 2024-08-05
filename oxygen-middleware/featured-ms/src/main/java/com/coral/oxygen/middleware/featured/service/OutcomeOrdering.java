package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import org.springframework.util.CollectionUtils;

public class OutcomeOrdering {

  private static final Comparator<OutputOutcome> OUTCOME_NAME_COMPARATOR = outcomeNameComparator();
  private static final Comparator<OutputOutcome> OUTCOME_PRICE_DEC_COMPARATOR =
      outcomePriceDecComparator();

  public void orderOutcomes(
      List<OutputOutcome> outcomes, boolean isLpAvailable, boolean sortByNonRunner) {
    if (isLpAvailable) {
      Collections.sort(
          outcomes,
          Comparator.comparing(this::outcomePrice, Comparator.nullsLast(Comparator.naturalOrder()))
              .thenComparing(
                  OutputOutcome::getName, Comparator.nullsLast(Comparator.naturalOrder())));
    } else {
      filterSpOutcomes(outcomes);
    }
    findFavourite(outcomes, "1");
    findFavourite(outcomes, "2");

    if (sortByNonRunner) {
      outcomes.forEach(
          o -> {
            if (o.getName() != null && o.getName().contains("N/R")) {
              o.setNonRunner(true);
            }
          });
      outcomes.sort(
          Comparator.comparing(
                  OutputOutcome::getNonRunner, Comparator.nullsFirst(Comparator.naturalOrder()))
              .thenComparing(this::compareByRunnerNumber));
    }
  }

  private int compareByRunnerNumber(OutputOutcome o1, OutputOutcome o2) {
    if (Boolean.TRUE.equals(o1.getNonRunner()) && Boolean.TRUE.equals(o2.getNonRunner())) {
      if (Objects.isNull(o1.getRunnerNumber())) {
        if (Objects.isNull(o2.getRunnerNumber())) {
          return 0;
        }
        return 1;
      } else if (Objects.isNull(o2.getRunnerNumber())) {
        return -1;
      } else {
        return o1.getRunnerNumber().compareTo(o2.getRunnerNumber());
      }
    }
    return 0;
  }

  private Double outcomePrice(OutputOutcome outcome) {
    if (Objects.isNull(outcome.getPrices()) || outcome.getPrices().isEmpty()) {
      return null;
    }
    OutputPrice outputPrice = outcome.getPrices().get(0);
    if (Objects.isNull(outputPrice)
        || Objects.isNull(outputPrice.getPriceNum())
        || Objects.isNull(outputPrice.getPriceDen())) {
      return null;
    }
    return 1.0 * outputPrice.getPriceNum() / outputPrice.getPriceDen() + 1;
  }

  /**
   * Finds outcome with according outcomeMeaningMinorCode and moves is to the end of the list
   *
   * @return {*}
   * @param outcomes
   * @param outcomeMeaningMinorCode
   */
  private void findFavourite(List<OutputOutcome> outcomes, String outcomeMeaningMinorCode) {
    outcomes.sort(
        Comparator.comparing(o -> outcomeMeaningMinorCode.equals(o.getOutcomeMeaningMinorCode())));
  }

  /*
   * find runner numbers
   * @param {array} outcomes
   * @return {number} number of outcome with runner numbers
   */
  private long findRunnerNumbers(List<OutputOutcome> outcomes) {
    return outcomes.stream().filter(o -> o.getRunnerNumber() != null).count();
  }

  /*
   * count outcomes that are not handicaps
   * @param {array} outcomes
   * @return {number} number of non favorite outcomes
   */
  private long getOutcomesCountWithoutFav(
      List<OutputOutcome> outcomes, Set<String> favMeaningMinorCodes) {
    return outcomes.stream()
        .filter(o -> !favMeaningMinorCodes.contains(o.getOutcomeMeaningMinorCode()))
        .count();
  }

  /*
   * filter SP available outcomes
   * @param {array} outcomes
   * @return {array} sorted outcomes
   */
  private void filterSpOutcomes(List<OutputOutcome> outcomes) {
    long runnerNumbers = findRunnerNumbers(outcomes);
    Set<String> favMeaningMinorCodes = new HashSet<>();
    favMeaningMinorCodes.add("1");
    favMeaningMinorCodes.add("2");
    long outcomesCountWithoutFav = getOutcomesCountWithoutFav(outcomes, favMeaningMinorCodes);
    if (runnerNumbers == outcomesCountWithoutFav) {
      Collections.sort(
          outcomes,
          Comparator.comparing(
              OutputOutcome::getRunnerNumber, Comparator.nullsFirst(Comparator.naturalOrder())));
    } else {
      Collections.sort(
          outcomes,
          Comparator.comparing(
              OutputOutcome::getName, Comparator.nullsLast(Comparator.naturalOrder())));
    }
  }

  public void orderRacingGridOutcomes(List<OutputOutcome> outcomes, boolean isSPOutcomes) {
    Comparator<OutputOutcome> comparator =
        isSPOutcomes ? OUTCOME_NAME_COMPARATOR : OUTCOME_PRICE_DEC_COMPARATOR;

    outcomes.sort(comparator);
  }

  private static Comparator<OutputOutcome> outcomeNameComparator() {
    return Comparator.comparing(OutputOutcome::getName);
  }

  private static Comparator<OutputOutcome> outcomePriceDecComparator() {
    return (o1, o2) -> {
      int result = 0;
      if (!CollectionUtils.isEmpty(o1.getPrices()) && !CollectionUtils.isEmpty(o2.getPrices())) {
        result = o1.getPrices().get(0).getPriceDec().compareTo(o2.getPrices().get(0).getPriceDec());
      }
      return result == 0 ? outcomeNameComparator().compare(o1, o2) : result;
    };
  }
}
