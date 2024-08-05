package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneOptinEmailAlreadyExistsException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesOptinEmailRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class FanzonesOptinEmailService extends AbstractService<FanzoneOptinEmail> {
  private final FanzonesOptinEmailRepository fanzonesOptinEmailRepository;
  private final FanzonesSycRepository fanzonesSycRepository;

  @Autowired
  public FanzonesOptinEmailService(
      FanzonesOptinEmailRepository fanzonesOptinEmailRepository,
      FanzonesSycRepository fanzonesSycRepository) {
    super(fanzonesOptinEmailRepository);
    this.fanzonesOptinEmailRepository = fanzonesOptinEmailRepository;
    this.fanzonesSycRepository = fanzonesSycRepository;
  }

  public Optional<FanzoneOptinEmail> findFanzoneOptinEmailByBrand(String brand) {
    return fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(brand);
  }

  public FanzoneOptinEmail getFanzoneOptinEmail(FanzoneOptinEmail dto, String brand) {
    Boolean isFanzoneOptinEmailCreated = checkFanzoneOptinEmail(brand);
    if (Boolean.TRUE.equals(isFanzoneOptinEmailCreated)) {
      throw new FanzoneOptinEmailAlreadyExistsException("Another FanzoneOptinEmail already exists");
    } else {
      return createFanzoneOptinEmail(dto, brand);
    }
  }

  private FanzoneOptinEmail createFanzoneOptinEmail(
      FanzoneOptinEmail fanzoneOptinEmail, String brand) {
    fanzoneOptinEmail.setBrand(brand);
    return fanzoneOptinEmail;
  }

  public Boolean checkFanzoneOptinEmail(String brand) {
    Optional<FanzoneOptinEmail> fanzoneOptinEmail =
        fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(brand);
    Boolean isFanzoneOptinEmailCreated = false;
    if (fanzoneOptinEmail.isPresent()) {
      isFanzoneOptinEmailCreated = true;
    }
    return isFanzoneOptinEmailCreated;
  }

  public FanzoneOptinEmail setSeasonStartAndEndDateFromFanzoneSyc(
      FanzoneOptinEmail fanzoneOptinEmail, String brand) {
    try {
      List<FanzoneSyc> fanzoneSyc = fanzonesSycRepository.findByBrand(brand);
      fanzoneOptinEmail.setSeasonStartDate(fanzoneSyc.get(0).getSeasonStartDate());
      fanzoneOptinEmail.setSeasonEndDate(fanzoneSyc.get(0).getSeasonEndDate());
    } catch (IndexOutOfBoundsException e) {
      log.error("fanzoneSyc doesnot exist  ", e);
    }
    return fanzoneOptinEmail;
  }
}
