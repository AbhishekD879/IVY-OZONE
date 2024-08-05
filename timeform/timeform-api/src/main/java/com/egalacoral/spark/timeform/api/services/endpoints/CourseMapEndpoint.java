package com.egalacoral.spark.timeform.api.services.endpoints;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface CourseMapEndpoint {

  @GET("racing/downloads/coursemap")
  Call<ResponseBody> getCourseMap(
      @Query("courseAbbrev") String courseAbbrev,
      @Query("raceTypeChar") String raceTypeChar,
      @Query("raceSurfaceChar") String raceSurfaceChar);
}
