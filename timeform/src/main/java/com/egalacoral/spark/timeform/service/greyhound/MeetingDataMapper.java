package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.Meeting;

public interface MeetingDataMapper {

  void map(Meeting meeting);

  void init();
}
