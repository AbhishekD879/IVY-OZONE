package com.ladbrokescoral.oxygen.utils;

import com.google.gson.Gson;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class MockUtil {

  public Object getMock() throws IOException {
    Gson gson = new Gson();
    new ClassPathResource("initial_data_mock.json");
    try (InputStreamReader leaderboardStream =
        new InputStreamReader(new ClassPathResource("initial_data_mock.json").getInputStream())) {
      @SuppressWarnings("unchecked")
      List<Object> leaderBoard = gson.fromJson(leaderboardStream, List.class);
      log.info("Object ", leaderBoard.toString());
      return leaderBoard;
    }
  }
}
