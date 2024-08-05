package com.egalacoral.spark.timeform.service.greyhound.mapper;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.service.greyhound.MeetingAbbreviationService;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

public class MeetingTypeMapperTest {

  private SiteServerAPI serverAPI;
  private MeetingAbbreviationService abbreviationService;

  @Before
  public void init() {
    abbreviationService = new MeetingAbbreviationService();
    abbreviationService.init();
    serverAPI = Mockito.mock(SiteServerAPI.class);
    List<Type> types = new ArrayList<>();
    Type e = createType(100, "test meeting");
    types.add(e);
    e = createType(200, "Nottingham GM");
    types.add(e);
    e = createType(300, "test greeting");
    types.add(e);
    Optional<List<Type>> optional = Optional.of(types);
    Mockito.when(serverAPI.getClassToSubType(Mockito.any(SimpleFilter.class))).thenReturn(optional);
  }

  protected Type createType(int id, String name) {
    Type e = Mockito.mock(Type.class);
    Mockito.when(e.getName()).thenReturn(name);
    Mockito.when(e.getId()).thenReturn(id);
    return e;
  }

  @Test
  public void testMap() {
    MeetingTypeMapper mapper = new MeetingTypeMapper(serverAPI, "20", abbreviationService);
    Meeting meeting = new Meeting();
    meeting.setName("test meeting");
    mapper.init();
    mapper.map(meeting);
    Assert.assertTrue(meeting.getOpenBetIds().contains(Integer.valueOf(100)));
  }

  @Test(expected = RuntimeException.class)
  public void testMapTypeListIsNotPresent() {
    Mockito.when(serverAPI.getClassToSubType(Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.empty());
    MeetingTypeMapper mapper = new MeetingTypeMapper(serverAPI, "20", abbreviationService);
    Meeting meeting = new Meeting();
    meeting.setName("test meeting");
    mapper.init();
    mapper.map(meeting);
    Assert.assertEquals(0, meeting.getOpenBetIds().size());
  }

  @Test
  public void testMapMeetingNameNotMatchedAnyType() {
    MeetingTypeMapper mapper = new MeetingTypeMapper(serverAPI, "20", abbreviationService);
    Meeting meeting = new Meeting();
    meeting.setName("test meeting 1");
    mapper.init();
    mapper.map(meeting);
    Assert.assertEquals(0, meeting.getOpenBetIds().size());
  }

  @Test
  public void testMapContains() {
    MeetingTypeMapper mapper = new MeetingTypeMapper(serverAPI, "20", abbreviationService);
    Meeting meeting = new Meeting();
    meeting.setName("test");
    mapper.init();
    mapper.map(meeting);
    Assert.assertTrue(meeting.getOpenBetIds().contains(Integer.valueOf(100)));
  }

  @Test
  public void testMapAbbreviations() {
    MeetingTypeMapper mapper = new MeetingTypeMapper(serverAPI, "20", abbreviationService);
    Meeting meeting = new Meeting();
    meeting.setName("Notts");
    mapper.init();
    mapper.map(meeting);
    Assert.assertTrue(meeting.getOpenBetIds().contains(Integer.valueOf(200)));
  }

  @Test
  public void testMapMultiple() {
    MeetingTypeMapper mapper = new MeetingTypeMapper(serverAPI, "20", abbreviationService);
    Meeting meeting = new Meeting();
    meeting.setName("test");
    mapper.init();
    mapper.map(meeting);
    Assert.assertTrue(meeting.getOpenBetIds().contains(Integer.valueOf(100)));
    Assert.assertTrue(meeting.getOpenBetIds().contains(Integer.valueOf(300)));
  }
}
