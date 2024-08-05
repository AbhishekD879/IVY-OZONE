package com.ladbrokescoral.oxygen.cms.api.service.showdown;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.ContestStatus;
import java.io.IOException;
import java.util.Optional;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Protocol;
import okhttp3.Request;
import okhttp3.ResponseBody;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import retrofit2.Call;
import retrofit2.Response;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {ShowdownService.class})
class ShowdownServiceTest {

  @MockBean private OkHttpClient okHttpClient;
  @MockBean private ShowdownEndPoint showdownEndPoint;
  @Autowired private ShowdownService showdownService;
  @Mock Call<ContestStatus> call;
  Response<ContestStatus> response;

  @BeforeEach
  void setUp() {
    ContestStatus contestStatus = new ContestStatus();
    contestStatus.setContestId("VmM2b0k1R3NUS0lmemNOSHNvdUphQT09");
    contestStatus.setEventId("2296007");
    contestStatus.setEntriesSize(10);
    contestStatus.setRegularTimeFinished(true);
    contestStatus.setRegularTimeFinished(true);
    response = Response.success(contestStatus);
  }

  @Test
  void testGetEntriesCount() throws IOException {
    ContestStatus req = new ContestStatus();
    req.setContestId("12345");
    req.setEventId("23434");
    when(showdownEndPoint.getContestStatus(any(), any())).thenReturn(call);
    when(call.execute()).thenReturn(response);
    assertNotNull(showdownService.getContestStatus("12345", "123"));
    assertEquals(10, showdownService.getContestStatus("12345", "123").get().getEntriesSize());
  }

  @Test
  void testGetEntriesCount_Error_Response_Null() throws IOException {
    Request request = new Request.Builder().url("http://shodown-url").build();
    when(showdownEndPoint.getContestStatus(any(), any())).thenReturn(call);
    when(call.execute()).thenReturn(null);
    when(call.request()).thenReturn(request);
    assertEquals(Optional.empty(), showdownService.getContestStatus("12345", "123"));
  }

  @Test
  void testGetEntriesCount_IOException() throws IOException {
    Request request = new Request.Builder().url("http://shodown-url").build();
    when(showdownEndPoint.getContestStatus(any(), any())).thenReturn(call);
    when(call.request()).thenReturn(request);
    when(call.execute()).thenThrow(IOException.class);
    assertEquals(Optional.empty(), showdownService.getContestStatus("12345", "123"));
  }

  @Test
  void testGetEntriesCount_Error_Response_Non_Null() throws IOException {
    Request request = new Request.Builder().url("http://shodown-url").build();
    okhttp3.Response rawResponse =
        new okhttp3.Response.Builder()
            .code(404)
            .request(request)
            .protocol(Protocol.HTTP_2)
            .message("Resource not found")
            .build();
    Response<ContestStatus> response2 =
        Response.error(ResponseBody.create(MediaType.parse("html"), "12345"), rawResponse);
    when(showdownEndPoint.getContestStatus(any(), any())).thenReturn(call);
    when(call.execute()).thenReturn(response2);
    when(call.request()).thenReturn(request);
    assertEquals(Optional.empty(), showdownService.getContestStatus("12345", "123"));
  }
}
