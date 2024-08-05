package com.egalacoral.spark.timeform.api.services.endpoints;

import com.egalacoral.spark.timeform.model.*;
import com.egalacoral.spark.timeform.model.internal.DataResponse;
import org.joda.time.DateTime;
import retrofit2.Call;
import retrofit2.http.FieldMap;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.QueryMap;

import java.util.Map;

public interface DataEndpoint {

  @GET("meetings")
  Call<DataResponse<Meeting>> getMeetings(@QueryMap(encoded = true) Map<String, String> params);

  @GET("tracks")
  Call<DataResponse<Track>> getTracks(@QueryMap(encoded = true) Map<String, String> params);

  @GET("races")
  Call<DataResponse<Race>> getRaces(@QueryMap(encoded = true) Map<String, String> params);

  @GET("greyhounds")
  Call<DataResponse<Greyhound>> getGreyhounds(@QueryMap(encoded = true) Map<String, String> params);

  @GET("entries")
  Call<DataResponse<Entry>> getEntries(@QueryMap(encoded = true) Map<String, String> params);

  @GET("performances")
  Call<DataResponse<Performance>> getPerformances(@QueryMap(encoded = true) Map<String, String> params);

}
