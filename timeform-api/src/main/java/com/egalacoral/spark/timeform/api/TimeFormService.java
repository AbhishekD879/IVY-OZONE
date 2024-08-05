package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.services.DataService;
import com.egalacoral.spark.timeform.api.services.endpoints.params.ExpandParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.FilterParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.MeetingDateEq;
import com.egalacoral.spark.timeform.api.services.endpoints.params.MeetingId;
import com.egalacoral.spark.timeform.api.services.endpoints.params.RaceId;
import com.egalacoral.spark.timeform.model.Entry;
import com.egalacoral.spark.timeform.model.Meeting;
import com.egalacoral.spark.timeform.model.Race;

import java.util.Date;
import java.util.List;

public class TimeFormService {

  private final DataService dataService;

  public TimeFormService(DataService dataService) {
    this.dataService = dataService;
  }

  public void getMeetingsForDate(Date date, DataCallback<List<Meeting>> callback) {
    dataService.requestMeetings(callback, FilterParam.create(new MeetingDateEq(date)));
  }

  public void getMeetingsWithRacesForDate(Date date, DataCallback<List<Meeting>> callback) {
    dataService.requestMeetings(callback, FilterParam.create(new MeetingDateEq(date)), new ExpandParam("races"));
  }
  public void getRacesByMeetingId(int meetingId, DataCallback<List<Race>> callback) {
    dataService.requestRaces(callback, FilterParam.create(MeetingId.eq(meetingId)));
  }

  public void getEntriesByRaceId(int raceId, DataCallback<List<Entry>> callback) {
    dataService.requestEntries(callback, FilterParam.create(RaceId.eq(raceId)));
  }

  public void getEntriesByMeetingDate(Date date, DataCallback<List<Entry>> callback){
    dataService.requestEntries(callback, FilterParam.create(new MeetingDateEq("race/meeting/", date)));
  }

  public void getEntries(DataCallback<List<Entry>> callback) {
    dataService.requestEntries(callback);
  }
  /**
   * For testing purposes. Will be removed soon
   * */
  @Deprecated
  public DataService getRAWService() {
    return dataService;
  }

  public int getPageSize() {
    return dataService.getPageSize();
  }

  public void setPageSize(int pageSize) {
    dataService.setPageSize(pageSize);
  }
}
