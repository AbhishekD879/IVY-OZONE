package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ObTypeDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualDto;
import com.ladbrokescoral.oxygen.cms.api.entity.VirtualNextEvent;
import com.ladbrokescoral.oxygen.cms.api.mapping.VirtualNextEventsMapper;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualNextEventsService;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * this controller is related to the Next_Events Carousel improvement in the Website EPIC ID --
 * OZONE-10268
 */
@RestController
public class VirtualNextEvents extends AbstractSortableController<VirtualNextEvent> {

  private final VirtualNextEventsService nextEventsService;

  public VirtualNextEvents(VirtualNextEventsService nextEventsService) {
    super(nextEventsService);
    this.nextEventsService = nextEventsService;
  }

  @GetMapping(value = "/virtual-next-event/{id}")
  public ResponseEntity<VirtualNextEvent> readById(@PathVariable("id") String id) {
    return new ResponseEntity<>(super.read(id), HttpStatus.OK);
  }

  @GetMapping(value = "/virtual-next-event/brand/{brand}")
  public ResponseEntity<List<VirtualNextEvent>> readEventsByBrand(
      @PathVariable("brand") String brand) {
    return new ResponseEntity<>(super.readByBrand(brand), HttpStatus.OK);
  }

  @GetMapping(value = "/virtual-next-event")
  public ResponseEntity<List<VirtualNextEvent>> readAllEvents() {
    return new ResponseEntity<>(super.readAll(), HttpStatus.OK);
  }

  @PostMapping(value = "/virtual-next-event")
  public ResponseEntity<VirtualNextEvent> saveEvents(@RequestBody @Validated VirtualDto body) {
    return super.create(VirtualNextEventsMapper.MAPPER.toEntity(body));
  }

  @PutMapping(value = "/virtual-next-event/{id}")
  public ResponseEntity<VirtualNextEvent> updateEvents(
      @PathVariable("id") String id, @RequestBody @Validated VirtualDto body) {
    return new ResponseEntity<>(
        super.update(id, VirtualNextEventsMapper.MAPPER.toEntity(body)), HttpStatus.OK);
  }

  @DeleteMapping(value = "/virtual-next-event/{id}")
  public ResponseEntity<VirtualNextEvent> deleteEvents(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("/virtual-next-event/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @GetMapping(value = "/virtual-next-event/{brand}/{classId}")
  public ResponseEntity<List<ObTypeDto>> getOBTypesForClass(
      @PathVariable("brand") String brand, @PathVariable("classId") String classId) {
    List<ObTypeDto> types =
        this.nextEventsService.getOBTypesForClass(brand, classId).stream()
            .sorted(Comparator.comparing(ObTypeDto::getTypeName))
            .collect(Collectors.toList());
    return new ResponseEntity<>(types, HttpStatus.OK);
  }
}
