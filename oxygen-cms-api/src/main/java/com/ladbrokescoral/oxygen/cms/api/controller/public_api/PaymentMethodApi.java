package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.PaymentMethodDto;
import com.ladbrokescoral.oxygen.cms.api.service.PaymentMethodService;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PaymentMethodApi implements Public {

  private final PaymentMethodService service;

  @Autowired
  public PaymentMethodApi(PaymentMethodService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/payment-methods")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<PaymentMethodDto> list =
        service.findByBrand(brand).stream()
            .map(
                s ->
                    new PaymentMethodDto(
                        s.isActive(), s.getName(), s.getIdentifier(), s.getSortOrder()))
            .collect(Collectors.toList());
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(Collections.emptyList(), HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
