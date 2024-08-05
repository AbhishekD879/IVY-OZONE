package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import com.ladbrokescoral.oxygen.cms.api.service.FaqService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FaqController extends AbstractSortableController<Faq> {
  private final FaqService service;

  @Autowired
  FaqController(FaqService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @PostMapping("faq")
  @Override
  public ResponseEntity create(@RequestBody @Valid Faq entity) {
    return super.create(entity);
  }

  @GetMapping("faq/brand/{brand}")
  @Override
  public List<Faq> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("faq/{id}")
  @Override
  public Faq read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("faq/{id}")
  @Override
  public Faq update(@PathVariable String id, @RequestBody Faq entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("faq/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  /** Create Order for Faq */
  @PostMapping("faq/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
