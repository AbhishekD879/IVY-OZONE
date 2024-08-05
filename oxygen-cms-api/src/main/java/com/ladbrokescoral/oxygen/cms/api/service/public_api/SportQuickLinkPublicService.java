package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SportQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.SportQuickLinkMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkExtendedRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SportQuickLinkPublicService {

  private final SportQuickLinkExtendedRepository repository;
  private final SegmentRepository segmentRepository;

  @Autowired
  public SportQuickLinkPublicService(
      SportQuickLinkExtendedRepository service, SegmentRepository segmentRepository) {
    this.repository = service;
    this.segmentRepository = segmentRepository;
  }

  public List<SportQuickLinkDto> findAll(String brand) {
    List<SportQuickLink> links = repository.findAll(brand);

    return enhanceToDtoWithSegments(brand, links);
  }

  public List<SportQuickLinkDto> enhanceToDtoWithSegments(
      String brand, List<SportQuickLink> links) {
    List<String> segments =
        segmentRepository.findByBrand(brand).stream()
            .map(Segment::getSegmentName)
            .collect(Collectors.toList());
    if (!segments.contains(SegmentConstants.UNIVERSAL)) segments.add(SegmentConstants.UNIVERSAL);

    return links.stream()
        .map(ql -> SportQuickLinkMapper.INSTANCE.toDto(ql, segments))
        .collect(Collectors.toList());
  }
}
