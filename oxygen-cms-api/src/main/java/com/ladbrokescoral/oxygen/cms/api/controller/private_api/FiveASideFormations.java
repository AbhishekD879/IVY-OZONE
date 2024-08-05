package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FiveASideFormation;
import com.ladbrokescoral.oxygen.cms.api.service.FiveASideFormationService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class FiveASideFormations extends AbstractSortableController<FiveASideFormation> {
  FiveASideFormations(FiveASideFormationService sortableService) {
    super(sortableService);
  }

  @Override
  @GetMapping("/fiveASide-formation")
  public List<FiveASideFormation> readAll() {
    return super.readAll();
  }

  @Override
  @GetMapping("fiveASide-formation/brand/{brand}")
  public List<FiveASideFormation> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @PostMapping("fiveASide-formation/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  @PostMapping("/fiveASide-formation")
  public ResponseEntity create(@Valid @RequestBody FiveASideFormation entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("/fiveASide-formation/{id}")
  public FiveASideFormation read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/fiveASide-formation/{id}")
  public FiveASideFormation update(
      @PathVariable("id") String id, @Valid @RequestBody FiveASideFormation updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("/fiveASide-formation/{id}")
  public ResponseEntity delete(@PathVariable("id") String id) {
    return super.delete(id);
  }
}
