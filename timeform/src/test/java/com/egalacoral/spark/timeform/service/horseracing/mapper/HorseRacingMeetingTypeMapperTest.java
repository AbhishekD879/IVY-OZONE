package com.egalacoral.spark.timeform.service.horseracing.mapper;

import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers;
import com.egalacoral.spark.timeform.service.greyhound.MeetingAbbreviationService;
import java.util.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HorseRacingMeetingTypeMapperTest {

  private HorseRacingMeetingTypeMapper mapper;

  @Mock private SiteServerAPI siteServerAPI;

  @Mock private MeetingAbbreviationService abbreviationService;

  @Before
  public void setUp() {
    mapper = new HorseRacingMeetingTypeMapper(siteServerAPI, "223", abbreviationService);
  }

  @Test
  public void testMaping() {
    HRMeeting meeting = new HRMeeting();
    meeting.setMeetingDate("Date");
    meeting.setCourseId(111);
    meeting.setCourseName("ABC meeting");

    List<Type> types = new ArrayList<>();
    types.add(new SiteServerDataWrappers.TypeForTest(1, "abc"));
    types.add(new SiteServerDataWrappers.TypeForTest(2, "Not matched"));
    types.add(new SiteServerDataWrappers.TypeForTest(3, "Additional ABC meeting"));

    Mockito.when(siteServerAPI.getClassToSubType(Mockito.any())).thenReturn(Optional.of(types));

    mapper.loadTypesFromOB();
    Set<Integer> obIdsForMeeting = mapper.getOBIdsForMeeting(meeting);

    Assert.assertEquals(2, obIdsForMeeting.size());
    Assert.assertTrue(obIdsForMeeting.contains(1));
    Assert.assertTrue(obIdsForMeeting.contains(3));
  }

  @Test
  public void testAbbreviations() {
    HRMeeting meeting = new HRMeeting();
    meeting.setMeetingDate("Date");
    meeting.setCourseId(111);
    meeting.setCourseName("ABC meeting");

    List<Type> types = new ArrayList<>();
    types.add(new SiteServerDataWrappers.TypeForTest(1, "XYZ"));
    types.add(new SiteServerDataWrappers.TypeForTest(2, "Not matched"));
    types.add(new SiteServerDataWrappers.TypeForTest(3, "Additional ABC meeting"));

    Mockito.when(abbreviationService.getAbbreviations(Mockito.anyString()))
        .thenReturn(Arrays.asList("matched"));
    Mockito.when(siteServerAPI.getClassToSubType(Mockito.any())).thenReturn(Optional.of(types));

    mapper.loadTypesFromOB();
    Set<Integer> obIdsForMeeting = mapper.getOBIdsForMeeting(meeting);

    Assert.assertEquals(2, obIdsForMeeting.size());
    Assert.assertTrue(obIdsForMeeting.contains(2));
    Assert.assertTrue(obIdsForMeeting.contains(3));
  }
}
