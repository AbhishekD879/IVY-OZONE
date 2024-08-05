package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticTextOtf;
import com.ladbrokescoral.oxygen.cms.api.service.StaticTextOtfService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class StaticTextOtfs extends AbstractSortableController<StaticTextOtf> {

  private StaticTextOtfService staticTextService;

  @Autowired
  StaticTextOtfs(StaticTextOtfService staticTextService) {
    super(staticTextService);
    this.staticTextService = staticTextService;
  }

  @PostMapping("static-text-otf")
  @Override
  public ResponseEntity create(@RequestBody @Valid StaticTextOtf entity) {
    return super.create(entity);
  }

  @GetMapping("static-text-otf")
  @Override
  public List<StaticTextOtf> readAll() {
    return super.readAll();
  }

  @GetMapping("static-text-otf/{id}")
  @Override
  public StaticTextOtf read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("static-text-otf/brand/{brand}")
  @Override
  public List<StaticTextOtf> readByBrand(@PathVariable String brand) {
    return staticTextService.findByBrand(brand);
  }

  @PutMapping("static-text-otf/{id}")
  @Override
  public StaticTextOtf update(@PathVariable String id, @RequestBody @Valid StaticTextOtf entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("static-text-otf/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("static-text-otf/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
