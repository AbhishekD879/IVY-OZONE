package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.services.DataService;
import com.egalacoral.spark.timeform.api.services.ImageService;
import com.egalacoral.spark.timeform.api.services.endpoints.params.*;
import com.egalacoral.spark.timeform.model.greyhound.*;
import com.egalacoral.spark.timeform.model.horseracing.*;
import com.egalacoral.spark.timeform.model.internal.DataResponse;
import java.util.Date;
import java.util.List;

public class TimeFormServiceImpl implements TimeFormService {

  private final DataService dataService;

  private final ImageService imageService;

  public TimeFormServiceImpl(DataService dataService, ImageService imageService) {
    this.imageService = imageService;
    this.dataService = dataService;
  }

  @Override
  public void getMeetingsForDate(Date date, DataCallback<List<Meeting>> callback) {
    dataService.requestMeetings(callback, FilterParam.create(new MeetingDateEq(date)));
  }

  @Override
  public void getRacesWithEntriesByMeetingDate(Date date, DataCallback<List<Race>> callback) {
    dataService.requestRaces(
        callback,
        FilterParam.create(new MeetingDateEq("meeting/", date)),
        new ExpandParams("entries"));
  }

  @Override
  public void getPerformancesByMeetingDate(Date date, DataCallback<List<Performance>> callback) {
    dataService.requestPerformances(
        callback,
        FilterParam.create(new MeetingDateEq("race/meeting/", date)),
        new ExpandParams("meeting"),
        new SelectParams("*", "meeting/meeting_date"));
  }

  public void getPerformancesMeetingsAfterDateForCreatingFormField(
      Date date, List<Integer> greyhoundIds, DataCallback<DataResponse<Performance>> callback) {
    dataService.requestPerformancesWithoutPagination(
        callback,
        FilterParam.create(
            new AndParams(new GreyhoundsIds(greyhoundIds), new MeetingDateAfter("meeting/", date))),
        new ExpandParams("meeting"),
        new SelectParams(
            "greyhound_full_name",
            "greyhound_id",
            "position_status",
            "meeting/meeting_date",
            "meeting_id"),
        new OrderParams("greyhound_id", "meeting_id desc"));
  }

  @Override
  public void getEntriesGreyhoundByMeetingDate(Date date, DataCallback<List<Entry>> callback) {
    dataService.requestEntries(
        callback,
        FilterParam.create(new MeetingDateEq("race/meeting/", date)),
        new ExpandParams("greyhound"),
        new SelectParams("greyhound", "entry_id"));
  }

  @Override
  public void getTracks(DataCallback<List<Track>> callback) {
    dataService.requestTracks(callback);
  }

  @Override
  public void getHRMeetingsForDate(Date date, DataCallback<List<HRMeeting>> callback) {
    dataService.requestHRMeetings(callback, FilterParam.create(new HRMeetingDateEq("", date)));
  }

  @Override
  public void getHRRacesWithRacesByMeetingDate(Date date, DataCallback<List<HRRace>> callback) {
    dataService.requestHRRaces(
        callback, FilterParam.create(new HRMeetingDateEq(date)), new ExpandParams("entries"));
  }

  @Override
  public void getHRPerformancesByMeetingDate(
      Date date, DataCallback<List<HRPerformance>> callback) {
    dataService.requestHRPerformances(
        callback, FilterParam.create(new HRMeetingDateEq(date)), new ExpandParams("jockey"));
  }

  @Override
  public void getHREntriesHorsesByMeetingDate(Date date, DataCallback<List<HREntry>> callback) {
    dataService.requestHREntries(
        callback,
        FilterParam.create(new HRMeetingDateEq(date)),
        new ExpandParams("horse"),
        new SelectParams("horse"));
  }

  @Override
  public void getHRCourses(DataCallback<List<HRCourse>> callback) {
    dataService.requestHRCourses(callback);
  }

  @Override
  public void getHRCountries(DataCallback<List<HRCountry>> callback) {
    dataService.requestHRCountries(callback);
  }

  @Override
  public void getHRCourseMapByRace(HRRace race, DataCallback<HRCourseMap> callback) {
    imageService.getCourseMap(
        race.getCourseAbbrev(), race.getRaceTypeChar(), race.getRaceSurfaceChar(), callback);
  }

  @Override
  public int getPageSize() {
    return dataService.getPageSize();
  }

  @Override
  public void setPageSize(int pageSize) {
    dataService.setPageSize(pageSize);
  }
}
