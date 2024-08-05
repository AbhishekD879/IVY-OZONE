package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostMessage;
import com.ladbrokescoral.oxygen.cms.api.exception.OddsBoostMessageCreateException;
import com.ladbrokescoral.oxygen.cms.api.service.OddsBoostMessageService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@Validated
public class OddsBoostMessagesController extends AbstractCrudController<OddsBoostMessage> {
  private final OddsBoostMessageService oddsBoostMessageService;
  private final ModelMapper mapper;

  public OddsBoostMessagesController(
      OddsBoostMessageService oddsBoostMessageService, ModelMapper mapper) {
    super(oddsBoostMessageService);
    this.oddsBoostMessageService = oddsBoostMessageService;
    this.mapper = mapper;
  }

  @PostMapping("/odds-boost-messages")
  public ResponseEntity<OddsBoostMessage> create(
      @Valid @RequestBody OddsBoostMessageDto oddsBoostMessageDto) {
    OddsBoostMessage oddsBoostMessage = mapper.map(oddsBoostMessageDto, OddsBoostMessage.class);
    try {
      oddsBoostMessage =
          oddsBoostMessageService.getOddsBoostMessage(
              oddsBoostMessage, oddsBoostMessage.getBrand());
      return super.create(oddsBoostMessage);
    } catch (OddsBoostMessageCreateException e) {
      throw new OddsBoostMessageCreateException("OddsBoostMessages is already present");
    }
  }

  @PutMapping("/odds-boost-messages/{id}")
  public OddsBoostMessage update(
      @PathVariable String id, @Valid @RequestBody OddsBoostMessageDto oddsBoostMessageDto) {
    OddsBoostMessage oddsBoostMessage = mapper.map(oddsBoostMessageDto, OddsBoostMessage.class);
    return super.update(id, oddsBoostMessage);
  }

  @GetMapping("/odds-boost-messages/brand/{brand}")
  public OddsBoostMessage findAllByBrand(@PathVariable @Brand String brand) {
    return oddsBoostMessageService.getByBrand(brand);
  }

  @DeleteMapping("/odds-boost-messages/{id}")
  public ResponseEntity<OddsBoostMessage> deleteById(@PathVariable String id) {
    return super.delete(id);
  }
}
