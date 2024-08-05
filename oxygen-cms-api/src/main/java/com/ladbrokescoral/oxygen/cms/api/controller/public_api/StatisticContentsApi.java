package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StatisticContentDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StatisticContentPublicService;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class StatisticContentsApi implements Public {

  private final StatisticContentPublicService service;

  @GetMapping("/{brand}/statistic-content/{eventId}")
  public ResponseEntity<List<StatisticContentDto>> getContentsByBrandAndEventId(
      @PathVariable("brand") String brand, @PathVariable("eventId") String eventId) {
    List<StatisticContentDto> contents =
        this.service.findAllByBrandAndEventId(brand, eventId).stream()
            .filter(this.service::filterContentsByTimeRange)
            .collect(Collectors.toList());
    return new ResponseEntity<>(contents, HttpStatus.OK);
  }
}
