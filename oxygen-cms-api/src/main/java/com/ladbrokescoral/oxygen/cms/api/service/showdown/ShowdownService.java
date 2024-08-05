package com.ladbrokescoral.oxygen.cms.api.service.showdown;

import com.ladbrokescoral.oxygen.cms.api.dto.ContestStatus;
import java.io.IOException;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import retrofit2.Call;
import retrofit2.Response;

@Slf4j(topic = "ShowdownService")
@Service
public class ShowdownService {
  private ShowdownEndPoint showdownEndPoint;

  @Autowired
  public ShowdownService(ShowdownEndPoint showdownEndPoint) {
    this.showdownEndPoint = showdownEndPoint;
  }

  public Optional<ContestStatus> getContestStatus(String eventId, String contestId) {
    return invokeSyncRequest(showdownEndPoint.getContestStatus(eventId, contestId));
  }

  public <T> Optional<T> invokeSyncRequest(Call<T> call) {
    try {
      Response<T> response = call.execute();
      return Objects.nonNull(response) && response.isSuccessful()
          ? Optional.ofNullable(response.body())
          : logError(call, response);
    } catch (IOException e) {
      log.error("Can't get data. Error occurred for URL {}", call.request().url(), e);
      return Optional.empty();
    }
  }

  private <T> Optional<T> logError(Call<T> call, Response<T> response) {
    if (Objects.nonNull(response)) {
      log.error(
          "Can't get data for URL {}. Response code: {}. Status: {}",
          call.request().url(),
          response.code(),
          response.message());
    } else {
      log.error("Can't get data. Response is null for URL {}", call.request().url());
    }
    return Optional.empty();
  }
}
