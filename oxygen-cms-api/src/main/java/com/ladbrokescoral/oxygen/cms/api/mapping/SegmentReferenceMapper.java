package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SegmentReferenceDto;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.ArrayList;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.CollectionUtils;

@Mapper
public interface SegmentReferenceMapper {
  SegmentReferenceMapper INSTANCE = Mappers.getMapper(SegmentReferenceMapper.class);

  @Mapping(target = "segment", source = "segmentName")
  @Mapping(target = "displayOrder", source = "sortOrder")
  SegmentReferenceDto toDto(SegmentReference entity);

  default List<String> getSegments(SegmentEntity entity, List<String> segments) {
    if (entity.isUniversalSegment()) {
      if (!CollectionUtils.isEmpty(entity.getExclusionList())) {
        List<String> segmentList = new ArrayList<>(segments);
        segmentList.removeAll(entity.getExclusionList());
        return segmentList;
      }
      return segments;
    } else {
      return entity.getInclusionList();
    }
  }

  default List<SegmentReferenceDto> getSegmentReferences(SegmentEntity entity) {
    List<SegmentReferenceDto> segmentReferences = new ArrayList<>();
    if (!CollectionUtils.isEmpty(entity.getSegmentReferences())) {
      entity.getSegmentReferences().stream()
          .filter(segRef -> segRef.getSortOrder() >= 0)
          .forEach(
              (SegmentReference segRef) -> {
                SegmentReferenceDto segmentReferenceDto = toDto(segRef);
                segmentReferences.add(segmentReferenceDto);
              });
    }
    return segmentReferences;
  }
}
