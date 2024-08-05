package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SegmentReferenceDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.CollectionUtils;

@Mapper(uses = DateMapper.class)
public interface SportQuickLinkMapper {

  SportQuickLinkMapper INSTANCE = Mappers.getMapper(SportQuickLinkMapper.class);

  @Mapping(target = "displayOrder", source = "sortOrder")
  SportQuickLinkDto toDto(SportQuickLink entity);

  SportQuickLinkDto copy(SportQuickLinkDto sportQuickLinkDto);

  default SportQuickLinkDto toDto(SportQuickLink sportQuickLink, List<String> segments) {
    SportQuickLinkDto sportQuickLinkDto = toDto(sportQuickLink);
    sportQuickLinkDto.setSegments(getSegments(sportQuickLink, segments));
    sportQuickLinkDto.setSegmentReferences(getSegmentReferences(sportQuickLink));
    sportQuickLinkDto.setFanzoneSegments(sportQuickLink.getFanzoneInclusions());
    return sportQuickLinkDto;
  }

  default List<String> getSegments(SportQuickLink sportQuickLink, List<String> segments) {
    if (sportQuickLink.isUniversalSegment()) {
      if (!CollectionUtils.isEmpty(sportQuickLink.getExclusionList())) {
        return segments.stream()
            .filter(seg -> !sportQuickLink.getExclusionList().contains(seg))
            .collect(Collectors.toList());
      }
      return segments;
    } else {
      return sportQuickLink.getInclusionList();
    }
  }

  default List<SegmentReferenceDto> getSegmentReferences(SportQuickLink sportQuickLink) {
    return CollectionUtils.isEmpty(sportQuickLink.getSegmentReferences())
        ? new ArrayList<>()
        : sportQuickLink.getSegmentReferences().stream()
            .map(this::toDto)
            .collect(Collectors.toList());
  }

  @Mapping(target = "segment", source = "segmentName")
  @Mapping(target = "displayOrder", source = "sortOrder")
  SegmentReferenceDto toDto(SegmentReference entity);
}
