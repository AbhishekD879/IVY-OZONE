package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.service.greyhound.MeetingFilterService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

@Component
public class HorseRacingMeetingFilterService extends MeetingFilterService {

  public HorseRacingMeetingFilterService(
      @Value("${horseracing.meetings.filter.file}") Resource resource) {
    super(resource);
  }

  @Override
  public boolean accept(String name) {
    return super.accept(name) || acceptableMeetingNames.isEmpty();
  }
}
