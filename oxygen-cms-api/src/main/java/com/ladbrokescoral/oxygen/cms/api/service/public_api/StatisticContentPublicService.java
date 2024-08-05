package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StatisticContentDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.StatisticContentMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.StatisticContentRepository;
import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class StatisticContentPublicService {

  private final StatisticContentRepository contentRepository;

  public List<StatisticContentDto> findAllByBrandAndEventId(String brand, String eventId) {

    return this.contentRepository.findAllByBrandAndEventIdOrderBySortOrderAsc(brand, eventId)
        .stream()
        .map(StatisticContentMapper.MAPPER::toDto)
        .collect(Collectors.toList());
  }

  public boolean filterContentsByTimeRange(StatisticContentDto dto) {
    return Instant.now().isAfter(dto.getStartTime()) && Instant.now().isBefore(dto.getEndTime());
  }
}
