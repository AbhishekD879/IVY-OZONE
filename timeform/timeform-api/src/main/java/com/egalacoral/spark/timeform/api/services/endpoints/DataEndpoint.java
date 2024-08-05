package com.egalacoral.spark.timeform.api.services.endpoints;

import com.egalacoral.spark.timeform.model.greyhound.*;
import com.egalacoral.spark.timeform.model.horseracing.*;
import com.egalacoral.spark.timeform.model.internal.DataResponse;
import java.util.Map;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;
import retrofit2.http.QueryMap;

public interface DataEndpoint {

  @GET("{path}/meetings")
  Call<DataResponse<Meeting>> getMeetings(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/tracks")
  Call<DataResponse<Track>> getTracks(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/races")
  Call<DataResponse<Race>> getRaces(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/greyhounds")
  Call<DataResponse<Greyhound>> getGreyhounds(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/entries")
  Call<DataResponse<Entry>> getEntries(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/performances")
  Call<DataResponse<Performance>> getPerformances(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  // For Horse Racing
  @GET("{path}/Meetings")
  Call<DataResponse<HRMeeting>> getHRMeetings(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/Races")
  Call<DataResponse<HRRace>> getHRRaces(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/Entries")
  Call<DataResponse<HREntry>> getHREntries(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/Performances")
  Call<DataResponse<HRPerformance>> getHRPerformances(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/Courses")
  Call<DataResponse<HRCourse>> getHRCourses(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);

  @GET("{path}/Countries")
  Call<DataResponse<HRCountry>> getHRCountries(
      @Path(value = "path", encoded = true) String urlSuffix,
      @QueryMap(encoded = true) Map<String, String> params);
}
