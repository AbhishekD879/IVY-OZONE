package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.TimeformMeeting;
import java.util.Collection;
import java.util.Date;

public interface MeetingService {

  Collection<? extends TimeformMeeting> getMeetingsByDate(Date date);
}
