package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.PaymentMethod;
import com.ladbrokescoral.oxygen.cms.api.repository.PaymentMethodRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class PaymentMethodService extends SortableService<PaymentMethod> {

  private final PaymentMethodRepository paymentMethodRepository;

  @Autowired
  public PaymentMethodService(final PaymentMethodRepository paymentMethodRepository) {
    super(paymentMethodRepository);
    this.paymentMethodRepository = paymentMethodRepository;
  }

  public List<PaymentMethod> findAllByBrand(String brand) {
    return paymentMethodRepository.findByBrand(brand);
  }
}
