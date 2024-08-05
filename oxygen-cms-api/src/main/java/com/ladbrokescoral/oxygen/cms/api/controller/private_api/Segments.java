package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SegmentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentPurgeService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.joda.time.Instant;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
public class Segments extends AbstractCrudController<Segment> {

  public final ModelMapper modelMapper;

  public final SegmentService service;
  public final SegmentPurgeService segmentPurgeService;

  public Segments(
      SegmentService service, ModelMapper modelMapper, SegmentPurgeService segmentPurgeService) {
    super(service);
    this.modelMapper = modelMapper;
    this.service = service;
    this.modelMapper
        .createTypeMap(SegmentDto.class, Segment.class)
        .addMapping(SegmentDto::getName, Segment::setSegmentName);
    this.modelMapper
        .createTypeMap(Segment.class, SegmentDto.class)
        .addMapping(Segment::getSegmentName, SegmentDto::setName);
    this.segmentPurgeService = segmentPurgeService;
  }

  @GetMapping("segments/brand/{brand}")
  public List<SegmentDto> getSegmentsByBrand(@PathVariable String brand) {
    List<SegmentDto> dtoList = new ArrayList<>();
    SegmentDto dto = new SegmentDto(SegmentConstants.UNIVERSAL, brand);
    dtoList.add(dto);
    dtoList.addAll(sortBySegmentNames(brand));
    return dtoList;
  }

  @PostMapping("segments")
  public ResponseEntity<Segment> saveSegment(@RequestBody SegmentDto dto) {
    return super.create(modelMapper.map(dto, Segment.class));
  }

  @PutMapping("segments/{id}")
  public Segment updateSegment(@RequestBody SegmentDto dto, @PathVariable String id) {
    return super.update(id, modelMapper.map(dto, Segment.class));
  }

  @DeleteMapping("/segments/{ids}/brand/{brand}")
  public void deleteSegments(@PathVariable List<String> ids, @PathVariable String brand) {
    List<String> segments = service.getSegmentsByIds(ids);
    Instant startTime = Instant.now();
    segmentPurgeService.deleteSegmentsInModules(segments, brand);
    Instant endTime = Instant.now();
    log.info("time consumed : " + (endTime.getMillis() - startTime.getMillis()));
    service.deleteByIds(ids);
  }

  private List<SegmentDto> sortBySegmentNames(String brand) {
    return super.readByBrand(brand).stream()
        .map(e -> this.modelMapper.map(e, SegmentDto.class))
        .filter(dto -> !SegmentConstants.UNIVERSAL.equals(dto.getName()))
        .sorted(Comparator.comparing(SegmentDto::getName, String.CASE_INSENSITIVE_ORDER))
        .collect(Collectors.toList());
  }
}
