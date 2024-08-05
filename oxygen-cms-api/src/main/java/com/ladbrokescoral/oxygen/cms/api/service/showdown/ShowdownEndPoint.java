package com.ladbrokescoral.oxygen.cms.api.service.showdown;

import com.ladbrokescoral.oxygen.cms.api.dto.ContestStatus;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Headers;
import retrofit2.http.Path;

public interface ShowdownEndPoint {

  @GET("contest/{eventId}/{contestId}")
  @Headers("Accept: application/json")
  Call<ContestStatus> getContestStatus(
      @Path("eventId") String eventId, @Path("contestId") String contestId);
}
