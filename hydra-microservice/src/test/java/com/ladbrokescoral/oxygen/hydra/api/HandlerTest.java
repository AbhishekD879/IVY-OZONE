package com.ladbrokescoral.oxygen.hydra.api;

import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.CoreMatchers.not;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import javax.servlet.http.HttpServletRequest;
import lombok.SneakyThrows;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
public class HandlerTest {

  @Autowired private MockMvc mvc;

  @MockBean private HttpServletRequest request;

  @SneakyThrows
  @Test
  public void testAlwaysReturn1stIP() {
    mvc.perform(get("/v1/session").header("X-Forwarded-For", " 192.168.0.1 ,  192.168.0.2"))
        .andExpect(status().isOk())
        .andExpect(content().string(containsString("192.168.0.1")))
        .andExpect(content().string(not(containsString("192.168.0.2"))));
  }

  @SneakyThrows
  @Test
  public void shouldReturnLocalHost() {
    mvc.perform(get("/v1/session"))
        .andExpect(status().isOk())
        .andExpect(content().string(containsString("127.0.0.1")));
  }

  @SneakyThrows
  @Test
  public void shouldUseRemoteAddr() {
    mvc.perform(
            get("/v1/session")
                .with(
                    request -> {
                      request.setRemoteAddr("192.168.0.11");
                      return request;
                    }))
        .andExpect(status().isOk())
        .andExpect(content().string(containsString("192.168.0.11")));
  }
}
