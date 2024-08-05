package com.egalacoral.spark.timeform.service.greyhound.mapper;

import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.service.greyhound.MeetingDataMapper;
import org.springframework.stereotype.Service;

/** Created by Igor.Domshchikov on 8/18/2016. */
@Service
public class MeetingNameMapper implements MeetingDataMapper {

  @Override
  public void map(Meeting meeting) {
    meeting.setName(meeting.getTrackShortName());
  }

  @Override
  public void init() {}
}
