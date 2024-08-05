package com.ladbrokescoral.oxygen.questionengine.service.impl;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.service.SiteServerService;

import java.lang.reflect.Method;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.apache.commons.io.IOUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SiteServerServiceImplTest {
  
  @Mock
  private SiteServerApi siteServerApi;
  
  private SiteServerService ssService;
  private Event event;

  @Before
  public void setUp() throws Exception {
    ssService = new SiteServerServiceImpl(siteServerApi);
    event = new ObjectMapper().readValue(
        IOUtils.toString(getClass().getResourceAsStream("/ss/__files/finished-event.json"), "UTF-8"), Event.class);
  
    when(siteServerApi.getCommentaryForEvent(anyList())).thenReturn(Optional.of(Collections.singletonList(event)));
  }

  @Test
  public void getFinishedEvent() {
    Optional<Event> finishedEvent = ssService.getEventDetails(anyString());
    
    assertTrue(finishedEvent.isPresent());
  }

  @Test
  public void findScoresForEvent() {
    List<Integer> scoresForEvent = ssService.findScoresForEvent(event);
    
    assertEquals(2, scoresForEvent.size());
    assertEquals(new Integer(3), scoresForEvent.get(0));
    assertEquals(new Integer(1), scoresForEvent.get(1));
  }

  @Test
  public void testEmptyCommentaryData() {
    List<Integer> scoresForEvent = ssService.findScoresForEvent(new Event());
    
    assertTrue(scoresForEvent.isEmpty());
  }

  @Test
  public void testWrongCommentaryData() {
    List<Children> children = event.getChildren();
    children.get(2).getEventParticipant().put("id", "123782145");

    List<Integer> scoresForEvent = ssService.findScoresForEvent(event);

    assertTrue(scoresForEvent.isEmpty());
  }

  @Test
  public void testIsResultedEvent() {
    boolean finishedEvent = ssService.isMatchFinished(event);

    assertTrue(finishedEvent);
  }

  @Test
  public void isMatchFinishedTestResultTrue() throws Exception{
    Method method =
            SiteServerServiceImpl.class.getDeclaredMethod("isMatchFinished", Event.class);
    method.setAccessible(true);
    method.invoke(ssService, event);
    assertNotNull(ssService);
  }

  @Test
  public void isMatchFinishedTestResultFalse() throws Exception{
    Method method =
            SiteServerServiceImpl.class.getDeclaredMethod("isMatchFinished", Event.class);
    method.setAccessible(true);
    event.setIsResulted(false);
    method.invoke(ssService, event);
    assertNotNull(ssService);
  }

  @Test
  public void isMatchFinishedTestResultNull() throws Exception{
    Method method =
            SiteServerServiceImpl.class.getDeclaredMethod("isMatchFinished", Event.class);
    method.setAccessible(true);
    event.setIsResulted(null);
    method.invoke(ssService, event);
    assertNotNull(ssService);
  }

}