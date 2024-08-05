package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewSignpostingCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSignpostingRepository;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Optional;
import javax.validation.constraints.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Component
@Validated
public class FanzonesNewSignpostingService extends AbstractService<FanzoneNewSignposting> {
  private FanzonesNewSignpostingRepository fanzonesNewSignpostingRepository;

  @Autowired
  public FanzonesNewSignpostingService(
      FanzonesNewSignpostingRepository fanzonesNewSignpostingRepository) {
    super(fanzonesNewSignpostingRepository);
    this.fanzonesNewSignpostingRepository = fanzonesNewSignpostingRepository;
  }

  private FanzoneNewSignposting createFanzoneNewSignposting(
      FanzoneNewSignposting fanzoneNewSignposting, String brand) {
    fanzoneNewSignposting.setBrand(brand);
    return fanzoneNewSignposting;
  }

  public Optional<FanzoneNewSignposting> findAllByBrand(String brand) {
    Optional<FanzoneNewSignposting> fanzoneNewSignposting =
        fanzonesNewSignpostingRepository.findAllByBrand(brand);
    if (fanzoneNewSignposting.isPresent()) {
      return fanzoneNewSignposting;
    } else {
      return Optional.of(new FanzoneNewSignposting());
    }
  }

  public FanzoneNewSignposting findAllByBrandAndId(String brand, String id) {
    Optional<FanzoneNewSignposting> fanzoneNewSignposting =
        fanzonesNewSignpostingRepository.findAllByBrandAndId(brand, id);
    return fanzoneNewSignposting.isPresent()
        ? fanzoneNewSignposting.get()
        : new FanzoneNewSignposting();
  }

  public Boolean checkFanzoneNewSignposting(String brand) {
    Optional<FanzoneNewSignposting> fanzoneNewSignposting =
        fanzonesNewSignpostingRepository.findAllByBrand(brand);
    Boolean isFanzoneNewSignpostingCreated = false;
    if (fanzoneNewSignposting.isPresent()) {
      isFanzoneNewSignpostingCreated = true;
    }
    return isFanzoneNewSignpostingCreated;
  }

  public FanzoneNewSignposting getFanzoneNewSignposting(FanzoneNewSignposting dto, String brand) {
    Boolean isFanzoneNewSignpostingCreated = checkFanzoneNewSignposting(brand);
    if (Boolean.TRUE.equals(isFanzoneNewSignpostingCreated)) {
      throw new FanzoneNewSignpostingCreateException(
          FZConstants.FANZONENEWSIGNPOSTING_ALREADYEXISTS);
    } else {
      return createFanzoneNewSignposting(dto, brand);
    }
  }

  public FanzoneNewSignposting populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull FanzoneNewSignposting entity) {
    Optional.ofNullable(entity.getCreatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userServiceObj::findOne)
        .ifPresent(user -> entity.setCreatedByUserName(user.getEmail()));

    Optional.ofNullable(entity.getUpdatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userServiceObj::findOne)
        .ifPresent(user -> entity.setUpdatedByUserName(user.getEmail()));
    return entity;
  }
}
