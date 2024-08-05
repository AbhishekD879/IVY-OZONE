package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.InplayStatsSortingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsSorting;
import com.ladbrokescoral.oxygen.cms.api.mapping.InplayStatsSortingMapper;
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsSortingService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class InplayStatsSortingController extends AbstractSortableController<InplayStatsSorting> {

  public InplayStatsSortingController(InplayStatsSortingService service) {
    super(service);
  }

  @PostMapping(value = "/inplay-stats-sorting")
  public ResponseEntity<InplayStatsSorting> saveEntity(
      @RequestBody @Validated InplayStatsSortingDto dto) {
    return super.create(InplayStatsSortingMapper.MAPPER.toEntity(dto));
  }

  @GetMapping(value = "/inplay-stats-sorting/{id}")
  public ResponseEntity<InplayStatsSorting> readEntityById(@PathVariable("id") String id) {
    return new ResponseEntity<>(super.read(id), HttpStatus.OK);
  }

  @GetMapping(value = "/inplay-stats-sorting/brand/{brand}")
  public ResponseEntity<List<InplayStatsSorting>> readEntitesByBrand(
      @PathVariable("brand") String brand) {
    return new ResponseEntity<>(super.readByBrand(brand), HttpStatus.OK);
  }

  @GetMapping(value = "/inplay-stats-sorting")
  public ResponseEntity<List<InplayStatsSorting>> readAllEntities() {
    return new ResponseEntity<>(super.readAll(), HttpStatus.OK);
  }

  @PutMapping(value = "/inplay-stats-sorting/{id}")
  public ResponseEntity<InplayStatsSorting> updateEntity(
      @PathVariable("id") String id, @RequestBody InplayStatsSortingDto dto) {
    return new ResponseEntity<>(
        super.update(id, InplayStatsSortingMapper.MAPPER.toEntity(dto)), HttpStatus.OK);
  }

  @DeleteMapping(value = "/inplay-stats-sorting/{id}")
  public ResponseEntity<InplayStatsSorting> deleteEntity(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("/inplay-stats-sorting/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
