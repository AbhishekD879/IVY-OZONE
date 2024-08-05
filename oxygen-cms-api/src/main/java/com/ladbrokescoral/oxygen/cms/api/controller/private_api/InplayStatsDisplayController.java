package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.InplayStatsDisplayDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsDisplay;
import com.ladbrokescoral.oxygen.cms.api.mapping.InplayStatsDisplayMapper;
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsDisplayService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class InplayStatsDisplayController extends AbstractSortableController<InplayStatsDisplay> {

  public InplayStatsDisplayController(InplayStatsDisplayService service) {
    super(service);
  }

  @PostMapping(value = "/inplay-stats-display")
  public ResponseEntity<InplayStatsDisplay> postEntity(
      @RequestBody @Validated InplayStatsDisplayDto dto) {
    return super.create(InplayStatsDisplayMapper.MAPPER.toEntity(dto));
  }

  @GetMapping(value = "/inplay-stats-display/{id}")
  public ResponseEntity<InplayStatsDisplay> readById(@PathVariable("id") String id) {
    return new ResponseEntity<>(super.read(id), HttpStatus.OK);
  }

  @GetMapping(value = "/inplay-stats-display/brand/{brand}")
  public ResponseEntity<List<InplayStatsDisplay>> readEntityByBrand(
      @PathVariable("brand") String brand) {
    return new ResponseEntity<>(super.readByBrand(brand), HttpStatus.OK);
  }

  @GetMapping(value = "/inplay-stats-display")
  public ResponseEntity<List<InplayStatsDisplay>> readAllEntities() {
    return new ResponseEntity<>(super.readAll(), HttpStatus.OK);
  }

  @PutMapping(value = "/inplay-stats-display/{id}")
  public ResponseEntity<InplayStatsDisplay> updateEntity(
      @PathVariable("id") String id, @RequestBody @Validated InplayStatsDisplayDto dto) {
    return new ResponseEntity<>(
        super.update(id, InplayStatsDisplayMapper.MAPPER.toEntity(dto)), HttpStatus.OK);
  }

  @DeleteMapping(value = "/inplay-stats-display/{id}")
  public ResponseEntity<InplayStatsDisplay> deleteEntity(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("/inplay-stats-display/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
