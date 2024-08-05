package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.HighlightCarouselDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.HighlightCarouselMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.HighlightCarouselRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class HighlightCarouselPublicService {

  private final HighlightCarouselRepository repository;
  private final SegmentRepository segmentRepository;

  /** Finds active Highlight Carousels per brand. */
  public List<HighlightCarouselDto> findActiveByBrand(String brand) {

    List<String> segments =
        segmentRepository.findByBrand(brand).stream()
            .map(Segment::getSegmentName)
            .collect(Collectors.toList());
    if (!segments.contains(SegmentConstants.UNIVERSAL)) segments.add(SegmentConstants.UNIVERSAL);

    return repository
        .findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(
            brand, Instant.now(), Instant.now())
        .stream()
        .collect(Collectors.groupingBy(HighlightCarousel::getSportId))
        .entrySet()
        .stream()
        .flatMap(carouselToSport -> carouselToSport.getValue().stream())
        .map(hc -> HighlightCarouselMapper.getInstance().toDto(hc, segments))
        .collect(Collectors.toList());
  }
}
