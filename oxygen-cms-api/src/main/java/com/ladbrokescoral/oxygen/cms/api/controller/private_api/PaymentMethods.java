package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PaymentMethod;
import com.ladbrokescoral.oxygen.cms.api.service.PaymentMethodService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class PaymentMethods extends AbstractSortableController<PaymentMethod> {

  @Autowired
  public PaymentMethods(PaymentMethodService sortableService) {
    super(sortableService);
  }

  @GetMapping("payment-methods/{id}")
  @Override
  public PaymentMethod read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("payment-methods/brand/{brand}")
  @Override
  public List<PaymentMethod> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("payment-methods")
  @Override
  public ResponseEntity create(@RequestBody PaymentMethod entity) {
    return super.create(entity);
  }

  @PutMapping("payment-methods/{id}")
  @Override
  public PaymentMethod update(@PathVariable String id, @RequestBody PaymentMethod entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("payment-methods/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("payment-methods/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
