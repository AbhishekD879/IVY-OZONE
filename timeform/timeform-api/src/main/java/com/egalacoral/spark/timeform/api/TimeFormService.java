package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.model.greyhound.*;
import com.egalacoral.spark.timeform.model.horseracing.*;
import com.egalacoral.spark.timeform.model.internal.DataResponse;
import java.util.Date;
import java.util.List;

public interface TimeFormService {

  void getMeetingsForDate(Date date, DataCallback<List<Meeting>> callback);

  void getRacesWithEntriesByMeetingDate(Date date, DataCallback<List<Race>> callback);

  void getPerformancesByMeetingDate(Date date, DataCallback<List<Performance>> callback);

  void getPerformancesMeetingsAfterDateForCreatingFormField(
      Date date, List<Integer> greyhoundIds, DataCallback<DataResponse<Performance>> callback);

  void getEntriesGreyhoundByMeetingDate(Date date, DataCallback<List<Entry>> callback);

  void getTracks(DataCallback<List<Track>> callback);

  void getHRMeetingsForDate(Date date, DataCallback<List<HRMeeting>> callback);

  void getHRRacesWithRacesByMeetingDate(Date date, DataCallback<List<HRRace>> callback);

  void getHRPerformancesByMeetingDate(Date date, DataCallback<List<HRPerformance>> callback);

  void getHREntriesHorsesByMeetingDate(Date date, DataCallback<List<HREntry>> callback);

  void getHRCourses(DataCallback<List<HRCourse>> callback);

  void getHRCountries(DataCallback<List<HRCountry>> callback);

  void getHRCourseMapByRace(HRRace race, DataCallback<HRCourseMap> callback);

  int getPageSize();

  void setPageSize(int pageSize);
}
