package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.EventHubControllerDto;
import com.ladbrokescoral.oxygen.cms.api.controller.mapping.EventHubControllerMapper;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.EventHub;
import com.ladbrokescoral.oxygen.cms.api.service.EventHubService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EventHubs extends AbstractSortableController<EventHub> {

  @Autowired
  public EventHubs(EventHubService crudService) {
    super(crudService);
  }

  @PostMapping("event-hub")
  public ResponseEntity create(@RequestBody @Validated EventHubControllerDto dto) {
    return super.create(EventHubControllerMapper.INSTANCE.toEntity(dto));
  }

  @GetMapping("event-hub")
  @Override
  public List<EventHub> readAll() {
    return super.readAll();
  }

  @GetMapping("event-hub/{id}")
  @Override
  public EventHub read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("event-hub/{id}")
  public EventHub update(
      @PathVariable String id, @RequestBody @Validated EventHubControllerDto dto) {
    return super.update(id, EventHubControllerMapper.INSTANCE.toEntity(dto));
  }

  @DeleteMapping("event-hub/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @Override
  @PostMapping("event-hub/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @GetMapping("event-hub/brand/{brand}")
  @Override
  public List<EventHub> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }
}
