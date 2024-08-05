package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.AccaInsuranceMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.AccaInsuranceMessage;
import com.ladbrokescoral.oxygen.cms.api.exception.AccaInsuranceMessageCreateException;
import com.ladbrokescoral.oxygen.cms.api.service.AccaInsuranceMessageService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class AccaInsuranceMessagesController extends AbstractCrudController<AccaInsuranceMessage> {
  private AccaInsuranceMessageService accaInsuranceMessageService;
  private ModelMapper mapper;

  @Autowired
  public AccaInsuranceMessagesController(
      AccaInsuranceMessageService accaInsuranceMessageService, ModelMapper mapper) {
    super(accaInsuranceMessageService);
    this.accaInsuranceMessageService = accaInsuranceMessageService;
    this.mapper = mapper;
  }

  @PostMapping("/acca-insurance-messages")
  public ResponseEntity<AccaInsuranceMessage> create(
      @Valid @RequestBody AccaInsuranceMessageDto accaInsuranceMessageDto) {
    AccaInsuranceMessage accaInsuranceMessage =
        mapper.map(accaInsuranceMessageDto, AccaInsuranceMessage.class);
    try {
      accaInsuranceMessage =
          accaInsuranceMessageService.getAccaInsuranceMessage(
              accaInsuranceMessage, accaInsuranceMessage.getBrand());
      return super.create(accaInsuranceMessage);
    } catch (AccaInsuranceMessageCreateException e) {
      throw new AccaInsuranceMessageCreateException("AccaInsuranceMessage is already present");
    }
  }

  @PutMapping("/acca-insurance-messages/{id}")
  public AccaInsuranceMessage update(
      @PathVariable String id,
      @Valid @RequestBody AccaInsuranceMessageDto accaInsuranceMessageDto) {
    AccaInsuranceMessage accaInsuranceMessage =
        mapper.map(accaInsuranceMessageDto, AccaInsuranceMessage.class);
    return super.update(id, accaInsuranceMessage);
  }

  @GetMapping("/acca-insurance-messages/brand/{brand}")
  public AccaInsuranceMessage findAllByBrand(@PathVariable @Brand String brand) {
    return accaInsuranceMessageService.getByBrand(brand);
  }

  @DeleteMapping("/acca-insurance-messages/{id}")
  public ResponseEntity<AccaInsuranceMessage> deleteById(@PathVariable String id) {
    return super.delete(id);
  }
}
