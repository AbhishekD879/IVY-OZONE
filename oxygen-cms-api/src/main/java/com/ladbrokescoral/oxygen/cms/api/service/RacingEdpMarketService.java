package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import com.ladbrokescoral.oxygen.cms.api.exception.RacingEdpValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.RacingEdpMarketRepository;
import java.util.List;
import java.util.function.Predicate;
import javax.validation.constraints.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
public class RacingEdpMarketService extends SortableService<RacingEdpMarket> {
  private final RacingEdpMarketRepository edpRepository;

  @Autowired
  public RacingEdpMarketService(RacingEdpMarketRepository edpRepository) {
    super(edpRepository);
    this.edpRepository = edpRepository;
  }

  /**
   * Check the scenarios for save and update entity.
   *
   * @param model
   * @return Same {@link RacingEdpMarket} object.
   * @throws RacingEdpValidationException if there are already two markets available with same name.
   */
  @Override
  public RacingEdpMarket prepareModelBeforeSave(RacingEdpMarket model) {
    validate(model);
    return model;
  }

  /** Add new element at the end of list */
  @Override
  protected boolean isNewElementCreatedFirstInTheList() {
    return false;
  }

  @NotNull
  private Predicate<RacingEdpMarket> getRacingEdpMarketPredicate(RacingEdpMarket model) {
    Predicate<RacingEdpMarket> filter = racingEdpMarket -> isSameHrOrGr(model, racingEdpMarket);
    // add filter if it is update market call.
    if (!StringUtils.isEmpty(model.getId())) {
      filter =
          racingEdpMarket ->
              !isSameMarket(model, racingEdpMarket) && isSameHrOrGr(model, racingEdpMarket);
    }
    return filter;
  }

  private boolean isSameMarket(RacingEdpMarket model, RacingEdpMarket racingEdpMarket) {
    return racingEdpMarket.getId().equalsIgnoreCase(model.getId());
  }

  private boolean isSameHrOrGr(RacingEdpMarket model, RacingEdpMarket racingEdpMarket) {

    return (racingEdpMarket.isGh() && model.isGh()) || (racingEdpMarket.isHr() && model.isHr());
  }

  private boolean isDuplicateHRAndGh(RacingEdpMarket racingEdpMarket) {
    Predicate<RacingEdpMarket> filter = getRacingEdpMarketPredicate(racingEdpMarket);
    return edpRepository.findByName(racingEdpMarket.getName()).stream()
            .filter(s -> s.getBrand().equalsIgnoreCase(racingEdpMarket.getBrand()))
            .filter(filter)
            .count()
        >= 1;
  }

  private boolean isMoreThanTwoMarkets(RacingEdpMarket racingEdpMarket) {
    return edpRepository.findByName(racingEdpMarket.getName()).stream()
            .filter(s -> s.getBrand().equalsIgnoreCase(racingEdpMarket.getBrand()))
            .count()
        > 1;
  }

  private void validate(RacingEdpMarket racingEdpMarket) {
    validateForCreateAndUpdate(racingEdpMarket);
    if (StringUtils.isEmpty(racingEdpMarket.getId())) {
      validateForCreate(racingEdpMarket);
    }
  }

  private void validateForCreateAndUpdate(RacingEdpMarket racingEdpMarket) {
    // There shouldn't be overriding isHR or isGR values of markets with same name.
    if (isDuplicateHRAndGh(racingEdpMarket)) {
      throw new RacingEdpValidationException(
          "There May be More than two items with same name or Market with same name in repo posses duplicate fields");
    }
  }

  private void validateForCreate(RacingEdpMarket racingEdpMarket) {
    // There shouldn't be more than two markets with same name. while creating new one.
    if (isMoreThanTwoMarkets(racingEdpMarket)) {
      throw new RacingEdpValidationException(
          "There May be More than two items with same name or Market with same name in repo posses duplicate fields");
    }
  }

  /** method for retrieving the markets by brand for RacingEdpMarketsApi */
  public List<RacingEdpMarket> findAllByBrandSorted(String brand) {
    return edpRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
