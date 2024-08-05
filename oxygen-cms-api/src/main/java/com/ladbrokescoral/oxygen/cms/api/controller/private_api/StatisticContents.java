package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.StatisticContentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StatisticContentTitleDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.StatisticContentMapper;
import com.ladbrokescoral.oxygen.cms.api.service.StatisticContentService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class StatisticContents extends AbstractSortableController<StatisticContent> {

  private final StatisticContentService service;

  public StatisticContents(StatisticContentService service) {
    super(service);
    this.service = service;
  }

  @GetMapping("/statistic-content/{brand}/{eventId}")
  public ResponseEntity<StatisticContentTitleDto> getTitle(
      @PathVariable("brand") String brand, @PathVariable("eventId") String eventId) {
    return new ResponseEntity<>(this.service.getTitleAndMarketIds(brand, eventId), HttpStatus.OK);
  }

  @PostMapping("/statistic-content")
  public ResponseEntity<StatisticContent> saveContent(
      @Validated @RequestBody StatisticContentDto dto) {
    return super.create(StatisticContentMapper.MAPPER.toEntity(dto));
  }

  @GetMapping("/statistic-content/{id}")
  public ResponseEntity<StatisticContent> readContent(@PathVariable("id") String id) {
    return new ResponseEntity<>(super.read(id), HttpStatus.OK);
  }

  @GetMapping("/statistic-content/event/{eventId}")
  public ResponseEntity<List<StatisticContent>> readContentByEventId(
      @PathVariable("eventId") String eventId) {
    List<StatisticContent> contentsByEventId = this.service.findByEventId(eventId);
    return CollectionUtils.isEmpty(contentsByEventId)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(contentsByEventId, HttpStatus.OK);
  }

  @GetMapping("/statistic-content")
  public ResponseEntity<List<StatisticContent>> readAllContent() {
    List<StatisticContent> contents = super.readAll();
    return CollectionUtils.isEmpty(contents)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(contents, HttpStatus.OK);
  }

  @GetMapping("/statistic-content/brand/{brand}")
  public ResponseEntity<List<StatisticContent>> readAllByBrand(
      @PathVariable("brand") String brand) {
    return new ResponseEntity<>(super.readByBrand(brand), HttpStatus.OK);
  }

  @PutMapping("/statistic-content/{id}")
  public ResponseEntity<StatisticContent> updateContent(
      @PathVariable("id") String id, @Validated @RequestBody StatisticContentDto dto) {
    return new ResponseEntity<>(
        super.update(id, StatisticContentMapper.MAPPER.toEntity(dto)), HttpStatus.OK);
  }

  @DeleteMapping("/statistic-content/{id}")
  public ResponseEntity<StatisticContent> deleteContent(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("/statistic-content/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
