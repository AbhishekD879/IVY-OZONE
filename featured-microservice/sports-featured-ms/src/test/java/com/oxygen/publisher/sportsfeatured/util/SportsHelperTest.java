package com.oxygen.publisher.sportsfeatured.util;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import com.oxygen.publisher.SocketIoTestHelper;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.model.module.EventInputDTO;
import org.junit.Before;
import org.junit.Test;

public class SportsHelperTest {

  private SocketIOClient client;
  private SportsCachedData sportsCachedData;
  private HandshakeData handshakeData;

  @Before
  public void init() {
    client = mock(SocketIOClient.class);
    sportsCachedData = mock(SportsCachedData.class);
    handshakeData = mock(HandshakeData.class);
  }

  @Test
  public void getEventInputForLogin() {
    EventInputDTO eventInputDTO = SportsHelper.getEventInputDTO(client, "16", true);
    assertEquals("16", eventInputDTO.getSportId());

    EventInputDTO inputDTO = SportsHelper.getEventInputDTO(client, "16#segment", true);
    assertEquals("16", inputDTO.getSportId());
    assertTrue(inputDTO.getSegmentId().isPresent());
    assertEquals("segment", inputDTO.getSegmentId().get());
  }

  @Test
  public void getEventInputForLoginException() {

    assertThrows(
        IllegalArgumentException.class,
        () -> SportsHelper.getEventInputDTO(client, "16#moduleId#segment", true));
  }

  @Test
  public void getEventInputForModule() {

    EventInputDTO eventInputDTO = SportsHelper.getEventInputDTO(client, "16#moduleId", false);
    assertEquals("16", eventInputDTO.getSportId());
    assertTrue(eventInputDTO.getModuleId().isPresent());
    assertEquals("moduleId", eventInputDTO.getModuleId().get());

    EventInputDTO eventInput = SportsHelper.getEventInputDTO(client, "16#moduleId#segment", false);
    assertEquals("16", eventInput.getSportId());
    assertTrue(eventInput.getModuleId().isPresent());
    assertEquals("moduleId", eventInput.getModuleId().get());
    assertTrue(eventInput.getSegmentId().isPresent());
    assertEquals("segment", eventInput.getSegmentId().get());
  }

  @Test
  public void getEventInputForModuleException() {

    assertThrows(
        IllegalArgumentException.class, () -> SportsHelper.getEventInputDTO(client, "16", false));
  }

  @Test
  public void checkValidSportId() {
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    PageRawIndex pageRawIndex = SportsHelper.checkValidSportId(client, sportsCachedData, "16");
    assertEquals("16", String.valueOf(pageRawIndex.getSportId()));
  }

  @Test
  public void checkValidSportIdException() {
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    assertThrows(
        IllegalArgumentException.class,
        () -> SportsHelper.checkValidSportId(client, sportsCachedData, "123"));
  }

  @Test
  public void getValidSportQueryParam() {
    when(client.getHandshakeData()).thenReturn(handshakeData);
    when(handshakeData.getSingleUrlParam("sportId")).thenReturn("16");
    String validSportQueryParam = SportsHelper.getValidSportQueryParam(client);

    assertEquals("16", validSportQueryParam);
  }

  @Test
  public void getValidSportQueryParamException() {
    when(client.getHandshakeData()).thenReturn(handshakeData);
    when(handshakeData.getSingleUrlParam("sportId")).thenReturn(null);
    assertThrows(
        IllegalArgumentException.class, () -> SportsHelper.getValidSportQueryParam(client));
  }
}
