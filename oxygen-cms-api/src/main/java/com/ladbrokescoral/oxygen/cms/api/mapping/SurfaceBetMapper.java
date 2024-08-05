package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.PriceDto;
import com.ladbrokescoral.oxygen.cms.api.dto.RelationDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SegmentReferenceDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Price;
import com.ladbrokescoral.oxygen.cms.api.entity.Relation;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.CollectionUtils;

@Mapper
public interface SurfaceBetMapper {

  static SurfaceBetMapper getInstance() {
    return SurfaceBetMapperInstance.SURFACE_BET_MAPPER_INSTANCE;
  }

  @Mapping(target = "displayOrder", source = "sortOrder")
  @Mapping(target = "reference", ignore = true)
  @Mapping(target = "selectionEvent", ignore = true)
  SurfaceBetDto toDto(SurfaceBet entity);

  PriceDto toDto(Price entity);

  PriceDto toDto(com.egalacoral.spark.siteserver.model.Price price);

  @Mapping(target = "relationType", source = "relatedTo")
  RelationDto toDto(Relation entity);

  SurfaceBetDto copy(SurfaceBetDto surfaceBetDto);

  final class SurfaceBetMapperInstance {
    private static final SurfaceBetMapper SURFACE_BET_MAPPER_INSTANCE =
        Mappers.getMapper(SurfaceBetMapper.class);

    private SurfaceBetMapperInstance() {}
  }

  /*
   * .filter( (Relation r) -> surfaceBet.isUniversalSegment() || (r.getRelatedTo()
   * == RelationType.sport && "0".equals(r.getRefId())))
   *
   * removed filter: All records to be shown in other than relationType and refId
   * sport and 0
   */

  default Stream<SurfaceBetDto> toDtoStream(SurfaceBet surfaceBet, List<String> segments) {
    return surfaceBet.getReferences().stream()
        .map(
            (Relation r) -> {
              SurfaceBetDto surfaceBetDto = toDto(surfaceBet);
              surfaceBetDto.setReference(toDto(r));
              surfaceBetDto.setSegments(getSegments(surfaceBet, segments));
              surfaceBetDto.setSegmentReferences(getSegmentReferences(surfaceBet, r.getId()));
              surfaceBetDto.setFanzoneSegments(surfaceBet.getFanzoneInclusions());
              return surfaceBetDto;
            });
  }

  default List<String> getSegments(SurfaceBet surfaceBet, List<String> segments) {
    if (surfaceBet.isUniversalSegment()) {
      if (!CollectionUtils.isEmpty(surfaceBet.getExclusionList())) {
        return segments.stream()
            .filter(seg -> !surfaceBet.getExclusionList().contains(seg))
            .collect(Collectors.toList());
      }
      return segments;
    } else {
      return surfaceBet.getInclusionList();
    }
  }

  default List<SegmentReferenceDto> getSegmentReferences(SurfaceBet surfaceBet, String pageRefId) {
    return CollectionUtils.isEmpty(surfaceBet.getSegmentReferences())
        ? new ArrayList<>()
        : surfaceBet.getSegmentReferences().stream()
            .filter(sbRef -> pageRefId.equals(sbRef.getPageRefId()))
            .map(this::toDto)
            .collect(Collectors.toList());
  }

  @Mapping(target = "segment", source = "segmentName")
  @Mapping(target = "displayOrder", source = "sortOrder")
  SegmentReferenceDto toDto(SegmentReference entity);
}
