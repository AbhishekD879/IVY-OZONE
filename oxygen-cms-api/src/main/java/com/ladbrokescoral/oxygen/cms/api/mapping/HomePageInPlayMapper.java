package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InplaySportDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SegmentReferenceDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.CollectionUtils;

@Mapper
public interface HomePageInPlayMapper {
  static HomePageInPlayMapper getInstance() {
    return HomePageInPlayMapperInstance.HOME_INPLAY_MAPPER_INSTANCE;
  }

  @Mapping(target = "displayOrder", source = "sortOrder")
  InplaySportDto toDto(HomeInplaySport entity);

  @Mapping(target = "segment", source = "segmentName")
  @Mapping(target = "displayOrder", source = "sortOrder")
  SegmentReferenceDto toDto(SegmentReference entity);

  InplaySportDto copy(InplaySportDto inplaySportDto);

  default InplaySportDto toDto(HomeInplaySport homeInplaySport, List<String> segments) {
    InplaySportDto inplaySportDto = toDto(homeInplaySport);
    inplaySportDto.setSegments(getSegments(homeInplaySport, segments));
    inplaySportDto.setSegmentReferences(getSegmentReferences(homeInplaySport));
    return inplaySportDto;
  }

  default List<String> getSegments(HomeInplaySport homeInplaySport, List<String> segments) {
    if (homeInplaySport.isUniversalSegment()) {
      if (!homeInplaySport.getExclusionList().isEmpty()) {
        return segments.stream()
            .filter(seg -> !homeInplaySport.getExclusionList().contains(seg))
            .collect(Collectors.toList());
      }
      return segments;
    } else {
      return homeInplaySport.getInclusionList();
    }
  }

  default List<SegmentReferenceDto> getSegmentReferences(HomeInplaySport homeInplaySport) {
    return CollectionUtils.isEmpty(homeInplaySport.getSegmentReferences())
        ? new ArrayList<>()
        : homeInplaySport.getSegmentReferences().stream()
            .map(this::toDto)
            .collect(Collectors.toList());
  }

  final class HomePageInPlayMapperInstance {
    private static final HomePageInPlayMapper HOME_INPLAY_MAPPER_INSTANCE =
        Mappers.getMapper(HomePageInPlayMapper.class);

    private HomePageInPlayMapperInstance() {}
  }
}
