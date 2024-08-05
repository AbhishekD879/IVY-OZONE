package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SegmentArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.bson.types.ObjectId;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class SegmentService extends AbstractService<Segment> {
  private final SegmentRepository segmentRepository;
  private final SegmentArchivalRepository segmentArchivalRepository;
  private ModelMapper modelMapper;

  public SegmentService(
      SegmentRepository segmentRepository,
      SegmentArchivalRepository segmentArchivalRepository,
      ModelMapper modelMapper) {
    super(segmentRepository);

    this.segmentRepository = segmentRepository;
    this.segmentArchivalRepository = segmentArchivalRepository;
    this.modelMapper = modelMapper;
  }

  public void createSegments(List<String> segmentNames, String brand) {
    List<Segment> segments =
        segmentNames.stream()
            .filter(
                segmentName ->
                    !segmentRepository.findByBrandAndSegmentName(brand, segmentName).isPresent())
            .map(
                segmentName ->
                    Segment.builder()
                        .segmentName(segmentName)
                        .brand(brand)
                        .isActive(true)
                        .archivalId(ObjectId.get().toHexString())
                        .build())
            .collect(Collectors.toList());

    segmentArchivalRepository.saveAll(
        super.save(segments).stream()
            .map(entity -> modelMapper.map(entity, SegmentArchive.class))
            .collect(Collectors.toList()));
  }

  public List<String> getSegmentsForSegmentedViews(String brand) {
    return segmentRepository.findByBrand(brand).stream()
        .map(Segment::getSegmentName)
        .filter(segment -> !SegmentConstants.UNIVERSAL.equalsIgnoreCase(segment))
        .collect(Collectors.toList());
  }

  public List<String> getSegmentsByIds(List<String> ids) {
    return segmentRepository.findAllByIdIn(ids).stream()
        .map(Segment::getSegmentName)
        .filter(segment -> !SegmentConstants.UNIVERSAL.equalsIgnoreCase(segment))
        .collect(Collectors.toList());
  }

  public void deleteByIds(List<String> ids) {
    segmentRepository.deleteByIdIn(ids);
  }
}
