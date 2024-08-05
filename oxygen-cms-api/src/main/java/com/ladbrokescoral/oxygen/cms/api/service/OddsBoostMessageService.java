package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostMessage;
import com.ladbrokescoral.oxygen.cms.api.exception.OddsBoostMessageCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.OddsBoostMessageRepository;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class OddsBoostMessageService extends AbstractService<OddsBoostMessage> {

  private OddsBoostMessageRepository oddsBoostMessageRepository;

  @Autowired
  public OddsBoostMessageService(OddsBoostMessageRepository oddsBoostMessageRepository) {
    super(oddsBoostMessageRepository);
    this.oddsBoostMessageRepository = oddsBoostMessageRepository;
  }

  public OddsBoostMessage getByBrand(String brand) {
    Optional<OddsBoostMessage> oddsBoostMessage = oddsBoostMessageRepository.findOneByBrand(brand);
    return oddsBoostMessage.isPresent() ? oddsBoostMessage.get() : new OddsBoostMessage();
  }

  public OddsBoostMessage getOddsBoostMessage(OddsBoostMessage oddsBoostMessage, String brand) {
    Boolean isOddsBoostMessageCreated = checkOddsBoostMessage(brand);
    if (Boolean.TRUE.equals(isOddsBoostMessageCreated)) {
      throw new OddsBoostMessageCreateException("OddsBoostMessages is already present");
    } else {
      return oddsBoostMessage;
    }
  }

  public Boolean checkOddsBoostMessage(String brand) {
    Optional<OddsBoostMessage> oddsBoostMessage = oddsBoostMessageRepository.findOneByBrand(brand);
    Boolean isOddsBoostMessageCreated = false;
    if (oddsBoostMessage.isPresent()) {
      isOddsBoostMessageCreated = true;
    }
    return isOddsBoostMessageCreated;
  }
}
