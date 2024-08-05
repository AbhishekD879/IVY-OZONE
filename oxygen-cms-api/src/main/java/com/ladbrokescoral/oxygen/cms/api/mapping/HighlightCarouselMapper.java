package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.HighlightCarouselDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SegmentReferenceDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.CollectionUtils;

@Mapper
public interface HighlightCarouselMapper {
  static HighlightCarouselMapper getInstance() {
    return HighlightCarouselMapperInstance.HIGHLIGHT_CAROUSEL_MAPPER_INSTANCE;
  }

  @Mapping(target = "displayOrder", source = "sortOrder")
  HighlightCarouselDto toDto(HighlightCarousel entity);

  @Mapping(target = "segment", source = "segmentName")
  @Mapping(target = "displayOrder", source = "sortOrder")
  SegmentReferenceDto toDto(SegmentReference entity);

  HighlightCarouselDto copy(HighlightCarouselDto highlightCarouselDto);

  default HighlightCarouselDto toDto(HighlightCarousel highlightCarousel, List<String> segments) {
    HighlightCarouselDto highlightCarouselDto = toDto(highlightCarousel);
    highlightCarouselDto.setSegments(getSegments(highlightCarousel, segments));
    highlightCarouselDto.setSegmentReferences(getSegmentReferences(highlightCarousel));
    highlightCarouselDto.setFanzoneSegments(highlightCarousel.getFanzoneInclusions());
    return highlightCarouselDto;
  }

  default List<String> getSegments(HighlightCarousel highlightCarousel, List<String> segments) {
    if (highlightCarousel.isUniversalSegment()) {
      if (!highlightCarousel.getExclusionList().isEmpty()) {
        return segments.stream()
            .filter(seg -> !highlightCarousel.getExclusionList().contains(seg))
            .collect(Collectors.toList());
      }
      return segments;
    } else {
      return highlightCarousel.getInclusionList();
    }
  }

  default List<SegmentReferenceDto> getSegmentReferences(HighlightCarousel highlightCarousel) {
    return CollectionUtils.isEmpty(highlightCarousel.getSegmentReferences())
        ? new ArrayList<>()
        : highlightCarousel.getSegmentReferences().stream()
            .map(this::toDto)
            .collect(Collectors.toList());
  }

  final class HighlightCarouselMapperInstance {
    private static final HighlightCarouselMapper HIGHLIGHT_CAROUSEL_MAPPER_INSTANCE =
        Mappers.getMapper(HighlightCarouselMapper.class);

    private HighlightCarouselMapperInstance() {}
  }
}
