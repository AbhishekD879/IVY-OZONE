package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AccaInsuranceMessage;
import com.ladbrokescoral.oxygen.cms.api.exception.AccaInsuranceMessageCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.AccaInsuranceMessageRepository;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AccaInsuranceMessageService extends AbstractService<AccaInsuranceMessage> {
  private AccaInsuranceMessageRepository accaInsuranceMessageRepository;

  @Autowired
  public AccaInsuranceMessageService(
      AccaInsuranceMessageRepository accaInsuranceMessageRepository) {
    super(accaInsuranceMessageRepository);
    this.accaInsuranceMessageRepository = accaInsuranceMessageRepository;
  }

  public AccaInsuranceMessage getByBrand(String brand) {
    Optional<AccaInsuranceMessage> accaInsuranceMessage =
        accaInsuranceMessageRepository.findOneByBrand(brand);
    return accaInsuranceMessage.isPresent()
        ? accaInsuranceMessage.get()
        : new AccaInsuranceMessage();
  }

  public AccaInsuranceMessage getAccaInsuranceMessage(
      AccaInsuranceMessage accaInsuranceMessage, String brand) {
    Boolean isAccaInsuranceMessageCreated = checkAccaInsuranceMessage(brand);
    if (Boolean.TRUE.equals(isAccaInsuranceMessageCreated)) {
      throw new AccaInsuranceMessageCreateException("AccaInsuranceMessage is already present");
    } else {
      return accaInsuranceMessage;
    }
  }

  public Boolean checkAccaInsuranceMessage(String brand) {
    Optional<AccaInsuranceMessage> accaInsuranceMessage =
        accaInsuranceMessageRepository.findOneByBrand(brand);
    Boolean isAccaInsuranceMessageCreated = false;
    if (accaInsuranceMessage.isPresent()) {
      isAccaInsuranceMessageCreated = true;
    }
    return isAccaInsuranceMessageCreated;
  }
}
